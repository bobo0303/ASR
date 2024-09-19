import torchaudio


def compute_wer(reference, hypothesis):  
    # Split the reference and hypothesis into words  
    ref_words = reference.split()  
    hyp_words = hypothesis.split()  
  
    # Create a matrix of zeros  
    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]  
  
    # Initialize the first row and column of the matrix  
    for i in range(len(ref_words) + 1):  
        d[i][0] = i  
    for j in range(len(hyp_words) + 1):  
        d[0][j] = j  
  
    # Populate the rest of the matrix  
    for i in range(1, len(ref_words) + 1):  
        for j in range(1, len(hyp_words) + 1):  
            substitution_cost = 0 if ref_words[i - 1] == hyp_words[j - 1] else 1  
            d[i][j] = min(  
                d[i - 1][j] + 1,  # deletion  
                d[i][j - 1] + 1,  # insertion  
                d[i - 1][j - 1] + substitution_cost  # substitution  
            )  
  
    # The bottom-right cell contains the edit distance  
    edit_distance = d[-1][-1]  
  
    # Calculate WER  
    wer_value = float(edit_distance) / len(ref_words)  
  
    return wer_value  

def compute_cer(reference, hypothesis):  
    # Create a matrix of zeros with dimensions (M+1)x(N+1), where M and N are the lengths of the reference and hypothesis strings  
    M = len(reference)  
    N = len(hypothesis)  
    distance_matrix = [[0] * (N + 1) for _ in range(M + 1)]  
  
    # Initialize the first row and first column of the matrix  
    for i in range(1, M + 1):  
        distance_matrix[i][0] = i  
    for j in range(1, N + 1):  
        distance_matrix[0][j] = j  
  
    # Populate the rest of the matrix with the edit distances  
    for i in range(1, M + 1):  
        for j in range(1, N + 1):  
            if reference[i - 1] == hypothesis[j - 1]:  
                cost = 0  
            else:  
                cost = 1  
            distance_matrix[i][j] = min(  
                distance_matrix[i - 1][j] + 1,     # Deletion  
                distance_matrix[i][j - 1] + 1,     # Insertion  
                distance_matrix[i - 1][j - 1] + cost  # Substitution  
            )  
  
    # The edit distance is in the bottom-right cell of the matrix  
    edit_distance = distance_matrix[M][N]  
  
    # CER is the edit distance divided by the length of the reference string  
    cer_value = edit_distance / M  
  
    return cer_value  


def get_wav_duration_torchaudio(wav_file_path: str) -> float:
    waveform, sample_rate = torchaudio.load(wav_file_path)
    # 持續時間 = (樣本數 / 取樣率)
    duration = waveform.size(1) / sample_rate
    return duration


def compute_real_time_factor(wav_file_path: str, process_time: float) -> float:
    input_time = get_wav_duration_torchaudio(wav_file_path)
    rtf = process_time / input_time
    return rtf

  



if __name__ == "__main__":
    # Example usage  
    reference_text = "this is a test"  
    hypothesis_text = "this is the test"  
    print(f"WER: {compute_wer(reference_text, hypothesis_text):.2%}")  


    # Example usage  
    reference_text = "hello world"  
    hypothesis_text = "h3llo w0rld"  
    print(f"CER: {compute_cer(reference_text, hypothesis_text):.2%}")  
