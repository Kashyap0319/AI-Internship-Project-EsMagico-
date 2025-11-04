"""
Document Processor Module
Handles PDF ingestion, text extraction, chunking, and embedding storage
Lightweight in-memory approach with disk caching for fast startup
"""

import logging
import pickle
import hashlib
from pathlib import Path
from typing import List, Tuple
import PyPDF2
import numpy as np
from sentence_transformers import SentenceTransformer
import config

# Set up logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Handles document ingestion and in-memory embedding storage with caching"""
    
    def __init__(self):
        """Initialize the document processor with embeddings model"""
        logger.info(f"Initializing DocumentProcessor with embedding model: {config.EMBEDDING_MODEL}")
        
        # Initialize embeddings model
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        
        # In-memory storage
        self.chunks = []  # List of text chunks
        self.embeddings = None  # Numpy array of embeddings
        self.metadata = []  # List of metadata dicts
        
        # Cache directory
        self.cache_dir = config.DATA_DIR / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        logger.info("Document processor initialized with caching enabled")
    
    def _get_cache_path(self, pdf_path: str) -> Path:
        """Get cache file path for a PDF"""
        pdf_file = Path(pdf_path)
        # Create hash of PDF path and modification time
        file_hash = hashlib.md5(f"{pdf_file.name}_{pdf_file.stat().st_mtime}".encode()).hexdigest()
        return self.cache_dir / f"{file_hash}.pkl"
    
    def _load_from_cache(self, pdf_path: str) -> Tuple[List[str], List[dict], np.ndarray]:
        """Load cached embeddings for a PDF"""
        cache_path = self._get_cache_path(pdf_path)
        
        if cache_path.exists():
            try:
                with open(cache_path, 'rb') as f:
                    cached_data = pickle.load(f)
                logger.info(f"✅ Loaded {len(cached_data['chunks'])} chunks from cache for {Path(pdf_path).name}")
                return cached_data['chunks'], cached_data['metadata'], cached_data['embeddings']
            except Exception as e:
                logger.warning(f"Cache load failed: {e}, will regenerate")
        
        return None, None, None
    
    def _save_to_cache(self, pdf_path: str, chunks: List[str], metadata: List[dict], embeddings: np.ndarray):
        """Save embeddings to cache"""
        cache_path = self._get_cache_path(pdf_path)
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump({
                    'chunks': chunks,
                    'metadata': metadata,
                    'embeddings': embeddings
                }, f)
            logger.info(f"💾 Cached {len(chunks)} chunks for {Path(pdf_path).name}")
        except Exception as e:
            logger.warning(f"Cache save failed: {e}")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as string
        """
        logger.info(f"Extracting text from: {pdf_path}")
        text = ""
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                    
            logger.info(f"Extracted {len(text)} characters from {num_pages} pages")
            return text
            
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
            return ""
    
    def chunk_text(self, text: str, source: str) -> List[Tuple[str, dict]]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Full text to chunk
            source: Source filename
            
        Returns:
            List of (chunk_text, metadata) tuples
        """
        chunks_with_metadata = []
        
        # Simple chunking by characters with overlap
        chunk_size = config.CHUNK_SIZE
        overlap = config.CHUNK_OVERLAP
        
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind('.')
                last_question = chunk.rfind('?')
                last_exclamation = chunk.rfind('!')
                
                break_point = max(last_period, last_question, last_exclamation)
                if break_point > chunk_size * 0.5:  # Only if we're past halfway
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            if chunk.strip():
                metadata = {
                    "source": source,
                    "chunk_id": chunk_id,
                    "start_char": start
                }
                chunks_with_metadata.append((chunk.strip(), metadata))
                chunk_id += 1
            
            start = end - overlap
        
        return chunks_with_metadata
    
    def process_pdfs(self, pdf_directory: str = None) -> int:
        """
        Process all PDFs and create in-memory embeddings with caching
        
        Args:
            pdf_directory: Path to directory containing PDFs
            
        Returns:
            Number of chunks processed
        """
        if pdf_directory is None:
            pdf_directory = config.PDF_DIR
            
        pdf_dir = Path(pdf_directory)
        if not pdf_dir.exists():
            logger.warning(f"PDF directory does not exist: {pdf_dir}")
            return 0
        
        pdf_files = list(pdf_dir.glob("*.pdf"))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_dir}")
            return 0
        
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        all_chunks = []
        all_metadata = []
        all_embeddings_list = []
        
        for pdf_file in pdf_files:
            try:
                # Try to load from cache first
                cached_chunks, cached_metadata, cached_embeddings = self._load_from_cache(str(pdf_file))
                
                if cached_chunks is not None:
                    # Use cached data
                    all_chunks.extend(cached_chunks)
                    all_metadata.extend(cached_metadata)
                    all_embeddings_list.append(cached_embeddings)
                else:
                    # Process PDF from scratch
                    logger.info(f"📄 Processing {pdf_file.name}...")
                    text = self.extract_text_from_pdf(str(pdf_file))
                    
                    if text:
                        # Chunk text
                        chunks_with_meta = self.chunk_text(text, pdf_file.name)
                        
                        pdf_chunks = []
                        pdf_metadata = []
                        
                        for chunk, meta in chunks_with_meta:
                            pdf_chunks.append(chunk)
                            pdf_metadata.append(meta)
                        
                        if pdf_chunks:
                            # Generate embeddings for this PDF
                            logger.info(f"🔄 Generating embeddings for {len(pdf_chunks)} chunks from {pdf_file.name}...")
                            pdf_embeddings = self.embedding_model.encode(
                                pdf_chunks,
                                show_progress_bar=True,
                                convert_to_numpy=True
                            )
                            
                            # Save to cache
                            self._save_to_cache(str(pdf_file), pdf_chunks, pdf_metadata, pdf_embeddings)
                            
                            # Add to collection
                            all_chunks.extend(pdf_chunks)
                            all_metadata.extend(pdf_metadata)
                            all_embeddings_list.append(pdf_embeddings)
                            
                            logger.info(f"✅ Created {len(pdf_chunks)} chunks from {pdf_file.name}")
                    
            except Exception as e:
                logger.error(f"Error processing {pdf_file.name}: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                continue
        
        if not all_chunks:
            logger.warning("No chunks created from PDFs")
            return 0
        
        # Combine all embeddings
        self.chunks = all_chunks
        self.metadata = all_metadata
        self.embeddings = np.vstack(all_embeddings_list) if all_embeddings_list else np.array([])
        
        logger.info(f"✨ Knowledge base ready with {len(self.chunks)} chunks from {len(pdf_files)} books")
        return len(self.chunks)
    
    def semantic_search(self, query: str, top_k: int = None) -> List[Tuple[str, dict, float]]:
        """
        Perform semantic search for relevant chunks
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of (chunk_text, metadata, similarity_score) tuples
        """
        if top_k is None:
            top_k = config.TOP_K_RESULTS
        
        if self.embeddings is None or len(self.chunks) == 0:
            logger.warning("No embeddings available for search")
            return []
        
        # Encode query
        query_embedding = self.embedding_model.encode([query], convert_to_numpy=True)[0]
        
        # Compute cosine similarities
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        # Return results
        results = []
        for idx in top_indices:
            results.append((
                self.chunks[idx],
                self.metadata[idx],
                float(similarities[idx])
            ))
        
        logger.info(f"Found {len(results)} relevant chunks for query: {query[:50]}...")
        return results
    
    def is_initialized(self) -> bool:
        """Check if knowledge base is loaded"""
        return self.embeddings is not None and len(self.chunks) > 0


# Global instance
_processor_instance = None

def get_processor() -> DocumentProcessor:
    """Get or create global document processor instance"""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = DocumentProcessor()
        _processor_instance.process_pdfs()
    return _processor_instance


if __name__ == "__main__":
    # Test the document processor
    processor = DocumentProcessor()
    count = processor.process_pdfs()
    
    print(f"\n✅ Processed {count} chunks from PDFs")
    
    # Test search
    test_query = "Tell me about Alice"
    results = processor.semantic_search(test_query, top_k=3)
    
    print(f"\n🔍 Test Query: {test_query}")
    print(f"Found {len(results)} relevant chunks:\n")
    
    for i, (chunk, meta, score) in enumerate(results, 1):
        print(f"Chunk {i} (Score: {score:.3f}, from {meta['source']}):")
        print(chunk[:200] + "...\n")
if __name__ == "__main__":
    # Test the document processor
    processor = DocumentProcessor()
    count = processor.process_pdfs()
    
    print(f"\n✅ Processed {count} chunks from PDFs")
    
    # Test search
    test_query = "Tell me about Alice"
    results = processor.semantic_search(test_query, top_k=3)
    
    print(f"\n🔍 Test Query: {test_query}")
    print(f"Found {len(results)} relevant chunks:\n")
    
    for i, (chunk, meta, score) in enumerate(results, 1):
        print(f"Chunk {i} (Score: {score:.3f}, from {meta['source']}):")
        print(chunk[:200] + "...\n")

