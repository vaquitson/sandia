from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

import os
from time import sleep
from datetime import *
import pickle

# necesarios para la fun generate_sport_object
all_sport_list = ("baile", "flow", "rpm", "yoga", "body combat", "tabata", "tabat", "body pump", "grit", "core",
                  "body attack", "sprint", "dance pad", "voley", "trekking", "trek", "basketball", "crosstrainning",
                  "escalada", "futbol", "gimnasio", "cros", "gim")

informacion_deportes = """ deportes a elegir:

    baile           body pump
    flow            grit
    rpm             core
    yoga            body attack
    body combat     sprint
    tabata          dance pad
    gimnasio

    crosstrainning  basketball 
    voley           escalada
    trekking        futbol


    si quieres agendar mas de un deporte a la semana ingresalos separados por una coma y sin espacio:
    ejemplo:
    voley, futbol, trekking, ...
    """

# necesarios para hour_day_sport_compiler
informacion_horarios = """estos son los bloques de horario
    09:00 - 10:00    bloque_1
    10:00 - 11:00    bloque_2
    11:30 - 12:30    bloque_3
    12:30 - 13:30    bloque_4
    13:00 - 14:00    bloque_5
    13:30 - 14:30    bloque_6
    14:15 - 15:15    bloque_7
    14:30 - 15:30    bloque_8 
    15:00 - 16:00    bloque_9
    15:30 - 16:30    bloque_10
    16:00 - 17:00    bloque_11
    17:00 - 18:00    bloque_12

dias: 
    lunes
    martes
    miercoles
    jueves 
    viernes
    """

valid_days = ("lunes", "martes", "miercoles", "jueves", "viernes", "0", "0")

# creamos un atupla con todos los boloques pobiles
valid_hour_bloks = []
for i in range(1, 13):
    valid_hour_bloks.append("bloque_{}".format(i))
tuple(valid_hour_bloks)


class Sport:
    def __init__(self, name):
        self.name = str(name)
        self.day_hour = {}

    def display_info(self):
        print(self.name)
        print(self.day_hour)

    def sport_name(self):
        sport_name = self.name
        return sport_name


def clear_console():
    os.system("cls")


def time_stamp(txt):
    print(txt, date_and_time())


def wait_unitl_hour():
    time_pos = 1
    while True:
        if date_and_time()[time_pos] == "20:00:04":
            print(date_and_time()[time_pos])
            break
        else:
            print(date_and_time())
            sleep(0.1)


def save_user_info():
    while True:
        user_name = input("ingresa tu mail de la U: ")
        print(" ")
        user_password = input("ingresa tu clave de la U: ")
        print("estamos comprobando tu informacion, esto podria tardar unos segundos")

        login_url = "https://intranet.uai.cl/Login.aspx"

        firefox_options = Options()
        firefox_options.add_argument("-headless")
        driverService = Service(r'./geckodriver.exe')
        driver = webdriver.Firefox(service=driverService, options=firefox_options)

        driver.get(login_url)

        sleep(0.3)
        usuario = driver.find_element(By.ID, "wucLogin1_tUsnNm")
        pass_word = driver.find_element(By.ID, "tUsrPaswd")

        usuario.send_keys(user_name)
        pass_word.send_keys(user_password)
        pass_word.send_keys(Keys.RETURN)
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "aspnetForm")))
            print("tun info se aguardado correctamente")
            driver.close()
            break
        except TimeoutException:
            print("ha habido un error con tu informacion intentalo de nuevo: ")
            driver.close()
    while True:
        valid_words = ("hombre", "mujer")
        sexo = input("cual es tu sexo (hombre/mujer)?: ")
        if sexo in valid_words:
            with open("./user_info.txt", "w") as text:
                text.write(user_name + "\n" + user_password + "\n" + sexo)
                text.close()
            print("sexo guardado con exito")
            break


def generate_sport_objetc():
    deporte = None
    sleep_time = 0.3
    sport_object_list = []
    break_main_while = True
    while break_main_while:
        break_main_while = False
        break_condition = True
        print(informacion_deportes)
        while break_condition:
            break_condition = False
            # preguntamos el deporte al usuario
            deporte = list(input("que deporte quieres agendar: ").split(", "))
            # comprobamos que los deportes son correctos
            for item in deporte:
                # si los deportes son incorrectos volvemos al segundo while
                if item not in all_sport_list:
                    sleep(sleep_time)
                    print("respuesta invalida: alguno de los deportes que elegiste no es correcto, intentalo de nuevo")
                    sleep(sleep_time)
                    break_condition = True
                # si los deportes so correctos creamos el objeto y rompemos el segundo while, manteniendo
                # break_condition = False
                elif item in all_sport_list:
                    if item == "body combat":
                        item = "combat"
                    elif item == "tabata":
                        item = "tabat"
                    elif item == "body pump":
                        item = "pump"
                    elif item == "body atack":
                        item = "atack"
                    elif item == "dance pad":
                        item = "pad"
                    elif item == "voley":
                        item = "vol"
                    elif item == "treekking":
                        item = "trek"
                    elif item == "basketball":
                        item = "basket"
                    elif item == "crosstrainning":
                        item = "cros"
                    elif item == "escalada":
                        item = "esca"
                    elif item == "futbol":
                        item = "futb"
                    elif item == "gimnasio":
                        item = "gim"
                    elif item == "yoga":
                        item = "yog"
                    sport_object_list.append(Sport(item))
        # feed back de los deportes elegidos
        clear_console()
        sleep(sleep_time)
        print("has elegido: {}".format(", ".join(deporte)))
        sleep(sleep_time)
        second_break_condition = True
        while second_break_condition:
            second_break_condition = False
            # preguntamos el usuario si quiere cambiar los deportes
            cambiar_deporte = input("quieres cambiar tus deportes (s/n): ")
            # comprobamos que la respuesta del usuario es correcta
            if cambiar_deporte != "s" and cambiar_deporte != "n":
                # si la respuesta es incorrecta volvemos al tercer while y repetimos el input
                print("respuesta invalida")
                second_break_condition = True
            # si el ususario queire cambiar su respuesta volvemos al main_while
            if cambiar_deporte == "s":
                clear_console()
                break_main_while = True
        clear_console()
        # finalmente retornamos los objetos y la lista de los deportes
        return sport_object_list


def hour_day_sport_compiler(sport_objects):
    copy_valid_days = list(valid_days).copy()
    clear_console()
    # imprimimos la info de los horarios
    print(informacion_horarios)
    # comensaos a unir deportes con hora y horarios
    for sport in sport_objects:
        first_while_break = True
        while first_while_break:
            first_while_break = False
            # recorremos la lista de objetos con los deportes
            sport_day = list(input("que dias quieres agendar {}: ".format(sport.name)).split(", "))
            for day in sport_day:
                if day not in valid_days:
                    print("ha habido un error con los dias, intentalo de nuevo")
                    first_while_break = True
                    break
                elif len(sport_day) != len(set(sport_day)):
                    print("no es valido reserva mas de una vez el mismo dia: intentalo de nuevo")
                    first_while_break = True
                    break
                elif day not in copy_valid_days:
                    print("ya elegiste esee dia en otro deporte: intentalo de nuevo ")
                    first_while_break = True
                    break
                else:
                    copy_valid_days.remove(day)
                    second_while_brek = True
                    while second_while_brek:
                        second_while_brek = False
                        day_hour = input("({}) en que bloque quieres agedar el dia {}: ".format(sport.name, day))
                        if day_hour not in valid_hour_bloks:
                            print("hubo un herror con el bloque que elegiste intentalo de nuevo: ")
                            second_while_brek = True
                        elif len(day_hour) < 2:
                            print("no puedes ir dos veces a deporte el mismo dia")
                            second_while_brek = True
                        else:
                            sport.day_hour[day] = day_hour
    return sport_objects


def save_the_desition():
    sport_objects = generate_sport_objetc()
    final_mesh = hour_day_sport_compiler(sport_objects)
    with open("./Sport_objects/Spors.pickle", "wb") as object_file:
        pickle.dump(final_mesh, object_file)
    print("tus horarios han sido guardados con exito :) ")


def load_Sport_object():
    with open("./Sport_objects/Spors.pickle", "rb") as object_file:
        # aqui se retorna la lista final con los objetos de deporte
        return pickle.load(object_file)


def scraping_fun(today_sport, today_hour):
    user_name_pos = 0
    user_password_pos = 1
    user_sex = 2
    txt = open("user_info.txt", "r")
    user_basic_info = txt.read().split("\n")

    if today_info()[0] is None:
        print("no hay deportes agndados el dia de hoy")
        home()

    if user_basic_info[user_sex] == "hombre":
        sexo = "muj"
    else:
        sexo = "homb"

    time_stamp("bot iniciado")
    login_url = "https://intranet.uai.cl/Login.aspx"
    reserve_url = "https://intranet.uai.cl/WebPages/Deporte/Reservas.aspx"

    firefox_options = Options()
    firefox_options.add_argument("-headless")
    driverService = Service(r'./geckodriver.exe')
    driver = webdriver.Firefox(service=driverService, options=firefox_options)

    driver.get(login_url)
    sleep(0.5)
    usuario = driver.find_element(By.ID, "wucLogin1_tUsnNm")
    pass_word = driver.find_element(By.ID, "tUsrPaswd")

    usuario.send_keys(user_basic_info[user_name_pos])
    pass_word.send_keys(user_basic_info[user_password_pos])
    pass_word.send_keys(Keys.RETURN)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "aspnetForm")))
        time_stamp("login terminado")
    except TimeoutException:
        pass
    # nos metemos a la pagina de reservas
    driver.get(reserve_url)
    time_stamp("entramos a las reservas")
    wait_unitl_hour()
    driver.refresh()

    main_css_selector_regex = "#ctl00_ContentPlaceHolder1_wucReservas_GrdReservas_ctl00__"
    sport_name_child = " > td:nth-child(3)"
    sport_hour_child = " td:nth-child(5)"
    slected_sport_match = []
    # nos aseguramos que esten disponibles las reservas
    while True:
        try:
            # comenzamos con el proseso de reservas
            # iteramos por todos los ID de los deportes
            for number in range(0, 51):
                try:
                    main_sport_id = driver.find_element(By.CSS_SELECTOR, main_css_selector_regex + str(number))
                    main_sport_name = driver.find_element(By.CSS_SELECTOR, main_css_selector_regex + str(number) +
                                                          sport_name_child)
                    if number == 0:
                        time_stamp("pagina cargada, iterando")
                    # comprobamos si el texto de del iterable coincide con el regex del nombre del deporte del dia
                    # coprobamos el largo porqeu la funcion findall agrega las coincidencias a una lista
                    if today_sport in main_sport_name.text.lower():
                        if sexo not in main_sport_name.text.lower():
                            slected_sport_match.append(main_sport_id)
                            if today_hour in main_sport_id.find_element(By.CSS_SELECTOR, sport_hour_child).text:
                                # tratamos de clikeaar el boton de reservas
                                while True:
                                    time_stamp("encontrmos el deporte y el horario")
                                    try:
                                        WebDriverWait(driver, 2).until(
                                            EC.presence_of_element_located((By.CLASS_NAME, "btn-Reservar")))
                                        time_stamp("el boton de reservas esta cargado")
                                    except TimeoutException:
                                        time_stamp("el boton de reservas no esta cargado")
                                        pass
                                    try:
                                        # esperamos a que exista elñ boton de reservas
                                        time_stamp("pre click")
                                        main_sport_id.find_element(By.CLASS_NAME, "btn-Reservar").click()
                                        time_stamp("pos click")
                                        WebDriverWait(driver, 180).until(
                                            EC.presence_of_element_located((By.CLASS_NAME, "btn-Cancelar")))
                                        time_stamp("hora tomada con exito")
                                        print("reeserva realizaada con exito", date_and_time())
                                        break
                                    # si el boton de reservas ya no existe lanzamos una exepcion no es clikeable
                                    except StaleElementReferenceException:
                                        time_stamp("StaleElementReferenceException linea 273")
                                        sleep(0.5)
                                        driver.refresh()
                                        pass
                                    # si el boton por alguna razon no existe
                                    except NoSuchElementException:
                                        sleep(0.5)
                                        driver.refresh()
                                        time_stamp("NoSuchElementException linea 279")
                                break
                            time_stamp("match sport")

                except NoSuchElementException:
                    time_stamp("ya no hay mas iterables en la pagina ")
                    break
            break
        except NoSuchElementException:
            time_stamp("no existe el ID, las reservas no estan habilitadas")
            driver.refresh()
    sleep(10)
    print("final ctm")
    driver.close()


def date_and_time():
    now = datetime.now()
    now_time = now.strftime("%H:%M:%S")
    now_day = now.weekday()
    return now_day, now_time


def day_int_convertor():
    POS_NOW_DAY = 0
    now_date_info = date_and_time()
    for day in valid_days:
        if now_date_info[POS_NOW_DAY] == 6:
            current_day = valid_days[0]
            return current_day
        elif now_date_info[POS_NOW_DAY] == valid_days.index(day):
            current_day = valid_days[valid_days.index(day) + 1]
            return current_day


def block_to_hour_convertor(today_block):
    if today_block == "bloque_1":
        regex_hour = "9:0"
        return regex_hour
    elif today_block == "bloque_2":
        regex_hour = "10:0"
        return regex_hour
    elif today_block == "bloque_3":
        regex_hour = "11:3"
        return regex_hour
    elif today_block == "bloque_4":
        regex_hour = "12:3"
        return regex_hour
    elif today_block == "bloque_5":
        regex_hour = "13:0"
        return regex_hour
    elif today_block == "bloque_6":
        regex_hour = "13:3"
        return regex_hour
    elif today_block == "bloque_7":
        regex_hour = "14:1"
        return regex_hour
    elif today_block == "bloque_8":
        regex_hour = "14:3"
        return regex_hour
    elif today_block == "bloque_9":
        regex_hour = "15:0"
        return regex_hour
    elif today_block == "bloque_10":
        regex_hour = "15:3"
        return regex_hour
    elif today_block == "bloque_11":
        regex_hour = "16:0"
        return regex_hour
    elif today_block == "bloque_12":
        regex_hour = "17:0"
        return regex_hour


def today_info():
    today_sport = None
    today_block = None
    today_hour = None

    now_week_day = day_int_convertor()

    sport_mesh_list = load_Sport_object()
    for sport in sport_mesh_list:
        try:
            if sport.day_hour[now_week_day]:
                today_sport = sport.sport_name()
                today_block = sport.day_hour[now_week_day]
                today_hour = block_to_hour_convertor(today_block)
        except KeyError:
            pass

    return today_sport, today_hour, today_block, now_week_day


def bullet_point():
    # 72000 son las 20:00 que serian lsa 9 aca menos 180 son las 19:57
    objective_time = 72000 - 140
    hour_pos = 1
    currente_hour = date_and_time()[hour_pos]
    time_list = currente_hour.split(":")

    current_time_second = int(time_list[0]) * pow(60, 2) + int(time_list[1]) * 60 + int(time_list[2])

    delay_time = objective_time - current_time_second

    print("sleeping for {}".format(delay_time / 3600))
    print(date_and_time())
    print("hora objetivo: 20:00:03")
    sleep(delay_time)


def home():
    print("HOME")
    if not os.path.exists("user_info.txt"):
        save_user_info()
        clear_console()
    if not os.path.exists("./Sport_objects/Spors.pickle"):
        save_the_desition()
        clear_console()

    valid_comands = ("CD", "SD", "CB", "RUN")
    while True:
        option = input()
        if option in valid_comands:
            break
        else:
            print("hubo un herror")
    if option == "CD":
        save_the_desition()
        input("preiona enter para continuar: ")
        clear_console()
        home()

    elif option == "SD":
        print(today_info())
        input("preiona enter para continuar: ")
        clear_console()
        home()

    elif option == "RUN":
        TODAY_SPORT_POS = 0
        TODAY_HOUR_POS = 1
        bullet_point()
        day_info = today_info()
        today_sport = day_info[TODAY_SPORT_POS]
        today_hour = day_info[TODAY_HOUR_POS]
        # comensamos el web scraping
        scraping_fun(today_sport, today_hour)
        input("preiona enter para continuar: ")
        clear_console()
        home()

    elif option == "CB":
        save_user_info()
        input("preiona enter para continuar: ")
        clear_console()


def main():
    home()


if __name__ == '__main__':
    main()
