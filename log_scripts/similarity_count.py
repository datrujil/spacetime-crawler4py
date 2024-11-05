import re

output_file_path = "similarity_count.txt"  # Keep this as a string for the file path

def load_fingerprints(filename):
    fingerprints = []
    current_url = None
    current_fingerprint = []
    
    with open(filename, 'r') as file:
        for line in file:
            url_match = re.match(r'(http[s]?://[^\s]+)', line)
            if url_match:
                # Save the previous fingerprint if it exists
                if current_url and current_fingerprint:
                    fingerprints.append((current_url, set(current_fingerprint)))
                # Start a new fingerprint for the new URL
                current_url = url_match.group(1)
                current_fingerprint = []
            else:
                # Attempt to parse line as fingerprint hashes
                if line.strip():  # Make sure the line isn't empty
                    try:
                        # Convert items to integers, ignore invalid ones
                        current_fingerprint.extend(
                            int(hash_value) for hash_value in line.strip().strip('[]').split(',') if hash_value.strip().isdigit()
                        )
                    except ValueError:
                        print(f"Warning: Could not parse fingerprint line: {line.strip()}")
        
        # Save the last fingerprint after finishing reading
        if current_url and current_fingerprint:
            fingerprints.append((current_url, set(current_fingerprint)))
    
    return fingerprints

def compute_similarity(fingerprint_a, fingerprint_b):
    # Calculate intersection and union of two fingerprints
    intersection = fingerprint_a & fingerprint_b
    union = fingerprint_a | fingerprint_b
    # Calculate similarity score
    return len(intersection) / len(union) if union else 0

def compare_all_files(fingerprint_file, similarity_threshold=0.75):
    # Load all fingerprints
    fingerprints = load_fingerprints(fingerprint_file)
    
    # Initialize dictionary to hold the similarity count for each URL
    # Use '_' to initialize each URL's value to 0
    similarity_counts = {url: 0 for url, _ in fingerprints}
    
    # Compare each pair (O(N^2) comparison)
    num_files = len(fingerprints)
    for i in range(num_files):
        url_a, fingerprint_a = fingerprints[i]
        for j in range(i + 1, num_files):
            url_b, fingerprint_b = fingerprints[j]
            if url_a == url_b:
                continue
            similarity = compute_similarity(fingerprint_a, fingerprint_b)
            # Increment counts for pairs with similarity above the threshold
            if similarity > similarity_threshold:
                similarity_counts[url_a] += 1
                similarity_counts[url_b] += 1

    with open(output_file_path, "a", encoding="utf-8") as output_file:
        for url, count in similarity_counts.items():
            if count > 0:
                output_file.write(f"{url}: {count} Similarities\n")

# Example: compare_all_files('fingerprint_content.txt', similarity_threshold=0.75)