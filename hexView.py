import argparse
import os
import re

# ANSI color codes
RESET = "\033[0m"
RED = "\033[31m"      # Non-printable bytes
YELLOW = "\033[33m"   # Repeating bytes
CYAN = "\033[36m"     # Null bytes
GREEN = "\033[32m"    # Search matches

def hex_view(file_path, bytes_per_line=16, start=0, length=None, search=None, search_str=None):
    """CLI hex viewer with color highlighting and search functionality."""
    try:
        with open(file_path, "rb") as f:
            f.seek(start)
            line_number = start // bytes_per_line
            bytes_read = 0

            # Convert search hex string to bytes if needed
            if search:
                search_bytes = bytes.fromhex(search)
            elif search_str:
                search_bytes = search_str.encode('latin-1')
            else:
                search_bytes = None

            prev_chunk = None

            while True:
                if length is not None:
                    to_read = min(bytes_per_line, length - bytes_read)
                    if to_read <= 0:
                        break
                    chunk = f.read(to_read)
                else:
                    chunk = f.read(bytes_per_line)

                if not chunk:
                    break

                # Hex representation with highlights
                hex_parts = []
                for i, b in enumerate(chunk):
                    hex_str = f"{b:02X}"
                    # Null byte highlight
                    if b == 0x00:
                        hex_str = f"{CYAN}{hex_str}{RESET}"
                    # Repeat byte highlight
                    elif prev_chunk and i < len(prev_chunk) and b == prev_chunk[i]:
                        hex_str = f"{YELLOW}{hex_str}{RESET}"
                    hex_parts.append(hex_str)
                hex_line = ' '.join(hex_parts)

                # ASCII representation
                ascii_parts = []
                for i, b in enumerate(chunk):
                    char = chr(b) if 32 <= b <= 126 else f"{RED}.{RESET}"
                    # Highlight search matches
                    if search_bytes:
                        for j in range(len(search_bytes)):
                            if i + j < len(chunk) and chunk[i:i+len(search_bytes)] == search_bytes:
                                char = f"{GREEN}{char}{RESET}"
                    ascii_parts.append(char)
                ascii_line = ''.join(ascii_parts)

                # Print line offset, hex, and ASCII
                print(f"{line_number*bytes_per_line:08X}  {hex_line:<{bytes_per_line*3}}  {ascii_line}")

                prev_chunk = chunk
                line_number += 1
                bytes_read += len(chunk)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Enhanced CLI Hex Viewer")
    parser.add_argument("-f", "--file", required=True, help="Path to the file to display")
    parser.add_argument("-b", "--bytes-per-line", type=int, default=16, help="Number of bytes per line")
    parser.add_argument("--start", type=int, default=0, help="Start byte offset")
    parser.add_argument("--length", type=int, help="Number of bytes to display")
    parser.add_argument("--search", help="Hex byte pattern to highlight, e.g., 'DEADBEEF'")
    parser.add_argument("--search-str", help="ASCII string to highlight")

    args = parser.parse_args()
    file_path = args.file

    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return

    hex_view(
        file_path,
        bytes_per_line=args.bytes_per_line,
        start=args.start,
        length=args.length,
        search=args.search,
        search_str=args.search_str
    )

if __name__ == "__main__":
    main()
