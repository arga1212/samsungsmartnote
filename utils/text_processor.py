import difflib
import re

def compare_texts(original_text, edited_text):
    """
    Compare original and edited texts to identify changes
    
    Parameters:
    ----------
    original_text : str
        Original text
    edited_text : str
        Edited text
        
    Returns:
    -------
    dict
        Statistics about changes
    list
        List of diff operations with details
    """
    # Clean text - remove extra whitespace and normalize line endings
    original_clean = re.sub(r'\s+', ' ', original_text).strip()
    edited_clean = re.sub(r'\s+', ' ', edited_text).strip()
    
    # Split into words
    original_words = original_clean.split()
    edited_words = edited_clean.split()
    
    # Use difflib to get differences
    matcher = difflib.SequenceMatcher(None, original_words, edited_words)
    diff = []
    
    # Statistics
    stats = {
        'added_words': 0,
        'removed_words': 0,
        'changed_words': 0
    }
    
    # Process diff operations
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            # Words were replaced
            original_segment = ' '.join(original_words[i1:i2])
            edited_segment = ' '.join(edited_words[j1:j2])
            diff.append({
                'operation': 'replace',
                'original': original_segment,
                'edited': edited_segment,
                'original_index': i1,
                'edited_index': j1,
                'original_length': i2-i1,
                'edited_length': j2-j1
            })
            stats['changed_words'] += max(i2-i1, j2-j1)
            
        elif tag == 'delete':
            # Words were deleted from original
            deleted_segment = ' '.join(original_words[i1:i2])
            diff.append({
                'operation': 'delete',
                'original': deleted_segment,
                'edited': '',
                'original_index': i1,
                'edited_index': j1,
                'original_length': i2-i1,
                'edited_length': 0
            })
            stats['removed_words'] += i2-i1
            
        elif tag == 'insert':
            # Words were added in edited
            inserted_segment = ' '.join(edited_words[j1:j2])
            diff.append({
                'operation': 'insert',
                'original': '',
                'edited': inserted_segment,
                'original_index': i1,
                'edited_index': j1,
                'original_length': 0,
                'edited_length': j2-j1
            })
            stats['added_words'] += j2-j1
    
    return stats, diff

def generate_highlighted_html(original_text, edited_text):
    """
    Generate HTML with highlighted differences
    
    Parameters:
    ----------
    original_text : str
        Original text
    edited_text : str
        Edited text
        
    Returns:
    -------
    str
        HTML content with highlighted differences
    """
    # Clean text - remove extra whitespace and normalize line endings
    original_clean = re.sub(r'\s+', ' ', original_text).strip()
    edited_clean = re.sub(r'\s+', ' ', edited_text).strip()
    
    # Split into words
    original_words = original_clean.split()
    edited_words = edited_clean.split()
    
    # Use difflib to get differences
    matcher = difflib.SequenceMatcher(None, original_words, edited_words)
    
    # Create HTML with spans
    html_output = []
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            # Equal parts
            text = ' '.join(original_words[i1:i2])
            html_output.append(text)
            
        elif tag == 'replace':
            # Words were replaced
            edited_segment = ' '.join(edited_words[j1:j2])
            html_output.append(f'<span class="changed">{edited_segment}</span>')
            
        elif tag == 'delete':
            # These words were in original but not in edited
            # Skip in the output
            pass
            
        elif tag == 'insert':
            # Words were added in edited
            inserted_segment = ' '.join(edited_words[j1:j2])
            html_output.append(f'<span class="added">{inserted_segment}</span>')
    
    return ' '.join(html_output)

def count_words(text):
    """
    Count words in text
    
    Parameters:
    ----------
    text : str
        Text to count words in
        
    Returns:
    -------
    int
        Word count
    """
    # Clean text and split into words
    clean_text = re.sub(r'\s+', ' ', text).strip()
    words = clean_text.split()
    return len(words)

def extract_keywords(text, max_keywords=10):
    """
    Extract important keywords from text
    
    This is a simple implementation based on word frequency.
    For production, consider using more advanced techniques like TF-IDF.
    
    Parameters:
    ----------
    text : str
        Text to extract keywords from
    max_keywords : int
        Maximum number of keywords to extract
        
    Returns:
    -------
    list
        List of keywords
    """
    # Clean text
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Split into words
    words = clean_text.split()
    
    # Filter out common stop words (simplified list)
    stop_words = {'dan', 'atau', 'di', 'ke', 'dari', 'yang', 'ini', 'itu', 'dengan', 'untuk', 'pada', 'adalah', 'dalam'}
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count word frequency
    word_freq = {}
    for word in filtered_words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    
    # Sort by frequency and return top keywords
    keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in keywords[:max_keywords]]