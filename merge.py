import fitz  # PyMuPDF
from pyzbar.pyzbar import decode,ZBarSymbol
from PIL import Image
import sys
import os
import shutil
import decimal


def extract_qrcodes_from_pdf(pdf_path):
    # 通过PyMuPDF打开PDF文件
    pdf_document = fitz.open(pdf_path)
    amout = 0
    invoiceNo = ""
    for page_number in range(pdf_document.page_count):
        print(f"Processing page {page_number + 1}")

        # 获取页面
        page = pdf_document[page_number]

        # 获取页面的图像（以RGB格式）
        pixmap = page.get_pixmap(dpi=300)
        pixmap.pil_save("./temp.png")

        
        # 使用pyzbar识别二维码
        decoded_objects = decode(Image.open("./temp.png"), symbols= [ZBarSymbol.QRCODE])


        for obj in decoded_objects:
            print(f"QR Code Data on page {page_number + 1}: {obj.data}")
            data = str(obj.data)
            data_array = data.split(",")
            if len(data_array) >=8:
                amout =  decimal.Decimal(data_array[4])
                invoiceNo=data_array[3]
        print(f"{amout},{invoiceNo}")
        os.remove("./temp.png")
    # 关闭PDF文件
    pdf_document.close()
    return (amout,invoiceNo)


def readDir(dir):
    resultList = []
    files = os.listdir(dir)
    for file in files:
        filename =dir+f"\\{file}"
        if file.__contains__("merge"):
            continue
        if file.__contains__(".pdf"):
            resultList.append(extract_qrcodes_from_pdf(filename))
    print(sum([x[0] for x in resultList]))
    mergeDir(dir)

def mergeDir(dir):
    mergedfile = dir+f"\\merged.pdf"
    if os.path.exists(mergedfile):
        os.remove(mergedfile)

    mergedPdf =None
    files = os.listdir(dir)
    for file in files:
        filename =dir+f"\\{file}"
        if file.__contains__("merge"):
            continue
        if mergedPdf is None:
           shutil.copy2(filename,mergedfile)
           mergedPdf = fitz.open(mergedPdf)
        else:
            p = fitz.open(filename)
            mergedPdf.insert_pdf(p)
            p.close()
    mergedPdf.save(mergedfile)
    mergedPdf.close()


if __name__ == "__main__":
    pdf_file_path = sys.argv[1]
    readDir(pdf_file_path)
    mergeDir(pdf_file_path)