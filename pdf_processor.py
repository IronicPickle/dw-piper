import re

def main():
  with open("./test.pdf", "rb") as pdf_file:
    pdf_data = str(pdf_file.read())
    stream_starts = [result for result in re.finditer("\n", pdf_data)]
    stream_ends = [result for result in re.finditer("\n", pdf_data)]

    #print(stream_starts)
    #print(stream_ends)

    print(pdf_data[stream_starts[0].span()[0]:stream_ends[0].span()[1]])

def stream_sort(span):
  return span[0]
      


if __name__ == "__main__": main()