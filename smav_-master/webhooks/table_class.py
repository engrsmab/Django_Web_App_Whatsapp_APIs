from pdf_creator import PDF
import datetime
from PyPDF2 import PdfFileReader

class PDF_Generation:
    def __init__(self) -> None:
        pass
    def get_pdf(self,item,device):
        title_data = [["T1","T2","H1","H2","On/Off","Battery Voltage","Gas","Wind","Time"]]
        try:
            pdf = PdfFileReader(f"{str(datetime.datetime.today().date())}.pdf")
        except:
            return self.create_pdf(item,device,title_data)
            
        
        data = pdf.pages[0].extractText()
        print("Extracted: ",data)
        data = data.split("T1T2H1H2On/OffBatteryVoltageGasWindTime")[-1].split(" ")
        print("Data: ",data)
        data.remove("")
        new_data = []
        count = len(data)
        counter = 0
        while count > 0:
            row = []
            for i in range(9):
                row.append(data[counter]+" ")
                counter += 1
                count -= 1
            new_data.append(row)
      
        
        
        for row in new_data:
            title_data.append(row)
        print(title_data)
        return self.create_pdf(item,device,title_data)
    def create_pdf(self,item,device,data):
        if int(item.machineStatus) < 12:
            machine = "OFF "
        else:
            machine = "ON "
        row_data = [str(item.temperature1)+" ",str(item.temperature2)+" ",str(item.humidity1)+" ",str(item.humidity2)+" ",machine,str(item.voltage)+" ",str(item.gas)+" ",str(item.wind)+" ",'{0}-GMT+0 '.format(item.datetime.strftime("%m/%d/%Y,%H:%M:%S"))]
        # row_data = [str(i)+" " for i in range(9)]
        print("Row Data: ",row_data)
        data.append(row_data)
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Times", size=10)

        pdf.create_table(table_data = data,title=f'Machine: {device}', cell_width='even')
        pdf.ln()
        pdf.output(f"{str(datetime.datetime.today().date())}.pdf")
        return True
import time
i = 1
pdf_class = PDF_Generation()
while True:
    print("Count: ",i)
    pdf_class.get_pdf("","Helium")
    time.sleep(5)
    i += 1
    if i == 3:
        break