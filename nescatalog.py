import os,struct,zipfile

def is_valid(value):

    if (value == "NES"):
        return "YES"
    else:
        return "NO"

def is_battery_present(value):

    if ((value & 0x2) != 0):
        return "YES"
    else:
        return "NO"

def is_trainer_present(value):

    if ((value & 0x4) != 0):
        return "YES"
    else:
        return "NO"

def get_mirroring(value):

    value &= 0x5
    if (value == 0x00):
        return "H MIRROR"
    elif (value == 0x01):
        return "V MIRROR"
    else:
        return "4 SCR VRAM"

html_file = open("nescatalog.htm", "w")
text_file = open("nescatalog.txt", "w")

counter = 0
template = "{0:7}{1:110}{2:6}{3:8}{4:8}{5:7}{6:11}{7:8}{8:8}{9:8}{10:8}\n"

html_head = '<html><head><link href="nescatalog.css" rel="stylesheet" type="text/css"></head><body><div class="datagrid"><table><thead><tr><th>#</th><th>FILE</th><th>VALID</th><th>PRG ROM</th><th>CHR ROM</th><th>MAPPER</th><th>MIRRORING</th><th>BATTERY</th><th>PRG RAM</th><th>TRAINER</th><th>FLAGS 7</th></tr></thead><tbody>'
html_foot = '</tbody></table></div></body></html>'

html_file.write(html_head)

for r,d,f in os.walk("."):
    f.sort()
    for files in f:
        file_path = files.lower()
        if file_path.endswith(".nes") or file_path.endswith(".zip"):
            rom_path = os.path.join(r, files)
            print (files)

            if ((counter % 100) == 0):
                text_file.write("====== ============================================================================================================= ===== ======= ======= ====== ========== ======= ======= ======= =======\n")
                text_file.write(template.format("#", "FILE", "VALID", "PRG ROM", "CHR ROM", "MAPPER", "MIRRORING", "BATTERY", "PRG RAM", "TRAINER", "FLAGS 7"))
                text_file.write("====== ============================================================================================================= ===== ======= ======= ====== ========== ======= ======= ======= =======\n")
            
            if file_path.endswith(".zip"):    
                zip_file = zipfile.ZipFile(files, "r")
                for rom_in_zip in zip_file.namelist():
                    rom = zip_file.read(rom_in_zip)
                    realsize = len(rom)
                    header = rom[:0x10]
                    break
            else:            
                rom_file = open(rom_path,"rb")
                header = rom_file.read(0x10)
                realsize = os.path.getsize(rom_path)
                rom_file.close()

            f_nes_id = header[0:0x4]
            f_prg_rom_size = header[0x4]
            f_chr_rom_size = header[0x5]
            f_flags_6 = header[0x6]
            f_flags_7 = header[0x7]
            f_prg_ram = header[0x8]
            f_flags_9 = header[0x9]
            f_flags_10 = header[0xA]
            f_padding = header[0xB:0x10]

            (b_nes_id,) = struct.unpack('4s', f_nes_id)
            nes_id = b_nes_id.decode("ascii", "ignore")
            nes_id = nes_id[:nes_id.find("\0")]

            (prg_rom_size,) = struct.unpack('B', f_prg_rom_size)
            (chr_rom_size,) = struct.unpack('B', f_chr_rom_size)
            (flags_6,) = struct.unpack('B', f_flags_6)
            (flags_7,) = struct.unpack('B', f_flags_7)
            (prg_ram,) = struct.unpack('B', f_prg_ram)
            (flags_9,) = struct.unpack('B', f_flags_9)
            (flags_10,) = struct.unpack('B', f_flags_10)

            mapper = (flags_6 >> 4) | (flags_7 & 0xF0)

            flags_7 &= 0x0F

            counter+=1

            text_file.write(template.format(str(counter), str(files), is_valid(nes_id), str(prg_rom_size), str(chr_rom_size), str(mapper), get_mirroring(flags_6), is_battery_present(flags_6), str(prg_ram), is_trainer_present(flags_6), format(flags_7, '#04x')))


            if ((counter % 2) == 1):
                html_file.write("<tr>")
            else:
                html_file.write('<tr class="alt">')
            
            html_file.write("<td>" + str(counter) + "</td><td>" + str(files) + "</td><td>" + is_valid(nes_id) + "</td><td>" + str(prg_rom_size) + "</td><td>" + str(chr_rom_size) + "</td><td>" + str(mapper) + "</td><td>" + get_mirroring(flags_6) + "</td><td>" + is_battery_present(flags_6) + "</td><td>" + str(prg_ram) + "</td><td>" + is_trainer_present(flags_6) + "</td><td>" + format(flags_7, '#04x') + "</td></tr>")
           
html_file.write(html_foot)

text_file.close()  
html_file.close()  
