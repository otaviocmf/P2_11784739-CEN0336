#!/usr/bin/env python3
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import nt_search
import hashlib

def find_longest_orf(sequence):
    start_codon = "ATG"
    stop_codons = ["TAA", "TAG", "TGA"]
    longest_orf = ""
    longest_orf_frame = None

    for frame in range(3):
        orf_start = sequence.find(start_codon, frame)
        
        while orf_start != -1:
            orf_end = -1
            for stop_codon in stop_codons:
                current_orf_end = sequence.find(stop_codon, orf_start + 3)
                if current_orf_end != -1 and (orf_end == -1 or current_orf_end < orf_end):
                    orf_end = current_orf_end

            if orf_end != -1:
                current_orf = sequence[orf_start:orf_end + 3]
                if len(current_orf) > len(longest_orf):
                    longest_orf = current_orf
                    longest_orf_frame = frame + 1  # Frames are 1-based

            orf_start = sequence.find(start_codon, orf_start + 3)

    return longest_orf, longest_orf_frame

def translate_sequence(sequence):
    # Ensure the sequence length is a multiple of three
    if len(sequence) % 3 != 0:
        sequence = sequence[:-(len(sequence) % 3)]

    return Seq(sequence).translate()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 script_getORF.py <input.fasta>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_fna_file = "ORF.fna"
    output_faa_file = "ORF.faa"

    try:
        with open(input_file, "r") as file:
            records = list(SeqIO.parse(file, "fasta"))

        processed_records = 0  # Counter for processed records

        with open(output_fna_file, "w") as fna_out, open(output_faa_file, "w") as faa_out:
            for record in records:
                print(f"Processing record: {record.id}")
                longest_orf, frame = find_longest_orf(record.seq)

                if longest_orf:
                    start = frame
                    end = start + len(longest_orf) * 3
                    frame_identifier = f"_frame{frame}_START{start}_END{end}"

                    # Writing to ORF.fna
                    fna_out.write(f">{record.id}{frame_identifier}\n{longest_orf}\n")

                    # Writing to ORF.faa
                    peptide = translate_sequence(longest_orf)
                    faa_out.write(f">{record.id}{frame_identifier}\n{peptide}\n")

                    print(f"Longest ORF: {longest_orf}")
                    print(f"Encoded Peptide: {peptide}")
                    processed_records += 1  # Increment the counter
                else:
                    print("No valid ORF found.")

        # Check for consistent number of entries
        if processed_records != len(records):
            print("Error: Number of entries in output files does not match the input.")
            sys.exit(1)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Calculating md5sum of the script
script_path = "script_getORF.py"
hash_md5 = hashlib.md5()
with open(script_path, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)

print(f"MD5sum of the script '{script_path}': {hash_md5.hexdigest()}")
