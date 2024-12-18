from django.shortcuts import render
from .models import *
from .utils import crear_pdf
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *
from django.core.files.base import ContentFile
from datetime import datetime
from.inserts import *
from docx import Document
import locale
import win32com.client
import pythoncom
from django.conf import settings
import os
from django.core.files import File
import json

def departamento_matricula(matricula):
    primer_letra = matricula[0:1:1]
    if primer_letra == "A":
        departamento = "Canelones"
    elif primer_letra == "B":
        departamento = "Maldonado"
    elif primer_letra == "C":
        departamento = "Rocha"
    elif primer_letra == "D":
        departamento = "Treina y Tres"
    elif primer_letra == "E":
        departamento = "Cerro Largo"
    elif primer_letra == "F":
        departamento = "Rivera"
    elif primer_letra == "G":
        departamento = "Artigas"
    elif primer_letra == "H":
        departamento = "Salto"
    elif primer_letra == "I":
        departamento = "Paysandú"
    elif primer_letra == "J":
        departamento = "Río Negro"
    elif primer_letra == "K":
        departamento = "Soriano"
    elif primer_letra == "L":
        departamento = "Colonia"
    elif primer_letra == "M":
        departamento = "San José"
    elif primer_letra == "N":
        departamento = "Flores"
    elif primer_letra == "O":
        departamento = "Florida"
    elif primer_letra == "P":
        departamento = "Lavalleja"
    elif primer_letra == "Q":
        departamento = "Durazno"
    elif primer_letra == "R":
        departamento = "Tacuarembó"
    elif primer_letra == "S":
        departamento = "Montevideo"
    else: 
        departamento = None
    return departamento

def pdf_crear(req,ruta_pdf,renderizar_en,model_insert,datos_a_pdf,nombre_archivo,mensaje,negocio):
    if negocio == "UM":
        logo = Logos.objects.get(id=1)
        logo_um_url = req.build_absolute_uri(logo.logo_UM.url) if logo.logo_UM else None

        logo_contexto = logo.logo_UM.url if logo.logo_UM else None
    else:
        logo = Logos.objects.get(id=2)
        logo_dm_url = req.build_absolute_uri(logo.logo_DM.url) if logo.logo_DM else None
        logo_contexto = logo.logo_DM.url if logo.logo_DM else None
        
    pdf = crear_pdf(ruta_pdf, datos_a_pdf)             
    if pdf:
         pdf_file = ContentFile(pdf.content)
         file_name = nombre_archivo
 # Asignar el archivo al campo identificacion_pdf de la moto
         model_insert.identificacion_pdf.save(file_name, pdf_file)
         model_insert.save()

    contexto = {
                "messages":mensaje,
                'pdf_url': model_insert.identificacion_pdf.url,
                "logo_um": logo_contexto

                }
    return render(req,"perfil_administrativo/motos/contenido_pdf.html",contexto)

def contexto_para_pdf_moto(model_moto,logo):
        datos_a_pdf = {
                        "moto": {
                            "id":model_moto.id,
                            "marca": model_moto.marca,
                            "modelo": model_moto.modelo,
                            "motor": model_moto.motor,
                            "anio": model_moto.anio,
                            "kilometros": model_moto.kilometros,
                            "precio": model_moto.precio
                        },
                        "current_year": datetime.now().year,
                            "logo_um": logo  # Asegúrate de importar datetime
                        }
        
        return datos_a_pdf

def checkbox_pdf(req,nueva_moto):
    ruta_pdf = "perfil_administrativo/motos/identificacion_moto.html"
    logo_um = Logos.objects.get(id=1)
    logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
    datos_a_pdf = contexto_para_pdf_moto(nueva_moto,logo_um_url)
    renderizar_en = "perfil_administrativo/motos/contenido_pdf.html"
    nombre_archivo = f"identificacion_{nueva_moto.id}.pdf"
    mensaje = "Moto ingresada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma."
    pdf_ret = pdf_crear(req,ruta_pdf,renderizar_en,nueva_moto,datos_a_pdf,nombre_archivo,mensaje,"UM")
    return pdf_ret

def validacion_moto(id_moto,num_motor,num_chasis):
    moto_actual = Moto.objects.filter(id = id_moto).first()
    existe_num_motor = Moto.objects.filter(num_motor = num_motor).first()
    existe_num_chasis = Moto.objects.filter(num_chasis = num_chasis).first()
    
    if existe_num_motor:
        if existe_num_motor.num_motor != moto_actual.num_motor:
            return "existe_num_motor"
    
    if existe_num_chasis:
        if existe_num_chasis.num_chasis != moto_actual.num_chasis:
            return "existe_num_chasis"
        
def matricula_valid(matricula,padron,id_moto):
    existe_matricula = Matriculas.objects.filter(matricula = matricula).first()
    # moto = Moto.objects.filter(num_motor = num_motor,num_chasis = num_chasis).first()
    if existe_matricula:
        if existe_matricula.moto_id != id_moto:
            return "matricula_existe"
    
    existe_padron = Matriculas.objects.filter(padron=padron).first()
    if existe_padron:
        if existe_padron.moto_id != id_moto:
            return "padron_existe"

def valid_cliente(documento,tel1,tel2,correo1,correo2):
    existe_cliente = Cliente.objects.filter(documento=documento).first()
    if existe_cliente:
        return "existe_cliente"
    
    existe_tel_1 = ClienteTelefono.objects.filter(telefono=tel1).first()

    if existe_tel_1:
        return "existe_telefono_1"
    
    if tel2:
        existe_tel_2 = ClienteTelefono.objects.filter(telefono=tel2).first()
        if existe_tel_2:
            return "existe_telefono_2"
    

    if correo1:
        existe_correo_1 = ClienteCorreo.objects.filter(correo=correo1).first()
        if existe_correo_1:
            return "existe_correo_1"
        
    if correo2:
        existe_correo_2 = ClienteCorreo.objects.filter(correo=correo2).first()
        if existe_correo_2:
            return "existe_correo_2"

def contexto_para_cliente(id_cliente,mensaje_error):
            cliente = Cliente.objects.get(id=id_cliente)
            tel_princ = ClienteTelefono.objects.get(principal=1,cliente_id=id_cliente)
            tel_sec = ClienteTelefono.objects.filter(principal=0,cliente_id=id_cliente).first()

            tipo_documento_ci = cliente.documento[0:2:1]
            tipo_documento_pas_dni = cliente.documento[0:3:1]

            longitud_doc = len(cliente.documento)
            doc_num = ""
            
            if tipo_documento_ci == "CI":
                #
                tipo_doc = "CI"
                for i in range(2,longitud_doc):
                    doc_num = doc_num + cliente.documento[i]
            elif tipo_documento_pas_dni == "DNI":
                tipo_doc = "DNI"
                for i in range(3,longitud_doc):
                    doc_num = doc_num + cliente.documento[i]
            else:
                tipo_doc = "PAS"
                for i in range(3,longitud_doc):
                    doc_num = doc_num + cliente.documento[i]
            
            correo_princ = ClienteCorreo.objects.filter(principal=1,cliente_id=id_cliente).first()
            correo_sec = ClienteCorreo.objects.filter(principal=0,cliente_id=id_cliente).first()

            if tel_sec:
                t_s = tel_sec.telefono
            else:
                t_s = None

            if correo_princ:
                longitud_correo_princ = len(correo_princ.correo)
                c_p = "" 
                lon = 0
                for i in range(0,longitud_correo_princ):
                    if correo_princ.correo[i] == "@":
                        j = i
                        break
                    else:
                        lon += 1
                        c_p = c_p + correo_princ.correo[i]
                
                longitud_dominio = longitud_correo_princ - lon
                dom_princ = ""
                pos = j
                for j in range(pos,longitud_correo_princ):
                    dom_princ = dom_princ + correo_princ.correo[j]
            else:
                c_p = ""
                dom_princ = None
            
            if correo_sec:
                
                longitud_correo_sec = len(correo_sec.correo)
                c_s = "" 
                lon = 0
                for i in range(0,longitud_correo_sec):
                    if correo_sec.correo[i] == "@":
                        j = i
                        break
                    else:
                        lon += 1
                        c_s = c_s + correo_sec.correo[i]
                
            
                dom_sec = ""
                pos = j
                for j in range(pos,longitud_correo_sec):
                    dom_sec = dom_sec + correo_sec.correo[j]
            else:
                c_s = ""
                dom_sec = None
            f_nac_formateada = cliente.fecha_nacimiento.strftime('%Y-%m-%d')
            contexto = {"datos_cliente":cliente,
                        "tipo_doc":tipo_doc,
                        "doc_num":doc_num,
                        "tel_princ":tel_princ,
                        "fecha_nac":f_nac_formateada,
                        "tel_sec":t_s,
                        "correo_princ":c_p,
                        "dom_princ":dom_princ,
                        "dom_sec":dom_sec,
                        "correo_sec":c_s,
                        "error_message":mensaje_error}
            return contexto

def valid_cliente_mod(id_cliente,documento,tel1,tel2,correo1,correo2):
    cliente_id = Cliente.objects.get(id=id_cliente)
    cliente_doc = Cliente.objects.filter(documento=documento).first()

    if cliente_doc:
        if id_cliente != cliente_doc.id:
            return "existe_cliente"
    
    tel_principal = ClienteTelefono.objects.filter(telefono=tel1).first()
    if tel_principal:
        if tel_principal.cliente_id != id_cliente:
            return "existe_tel_principal"
    
    tel_secundario = ClienteTelefono.objects.filter(telefono=tel2).first()
    if tel_secundario:
        if tel_secundario.cliente_id != id_cliente:
            return "existe_tel_secundario"
        
    correo_princ = ClienteCorreo.objects.filter(correo=correo1).first()
    if correo_princ:
        if correo_princ.cliente_id != id_cliente:
            return "existe_correo_principal"

    correo_sec = ClienteCorreo.objects.filter(correo=correo2).first()
    if correo_sec:
        if correo_sec.cliente_id != id_cliente:
            return "existe_correo_secundario"

def validar_personal(documento,telefono,correo):
    personal = Personal.objects.filter(documento=documento).first()
    if personal:
        #VERIFICAR SI EXISTE EN ADMINISTRATIVO
        administrativo = Administrativo.objects.filter(personal_ptr_id = personal.id).first()
        if administrativo:
            if administrativo.activo == 1: #SI EXISTIERA DEVUELVE ERROR 
                return "existe_admin"
            else: #SI EXISTIERA Y FUE DADO DE BAJA COMO ADMINISTRATIVO (EJ. FUE ADMIN, PASO A SER MECANICO Y VUELVE A SER ADMIN), SIMPLEMENTE SE MODIFICA EL CAMPO ACTIVO = 1
                return "admin_desactivado"
    
    telefono_pers = Personal.objects.filter(telefono = telefono).first()

    if telefono_pers: #SI EL TELEFONO DEL PERSONAL A INGRESAR EXISTIERA (PUEDE QUE SEA UN MECANICO QUE SE LE ASIGNARA TAREAS DE ADMINISTRATIVO), EL ADMINISTRATIVO LOGEADO EN EL SISTEMA DEBERA OTORGARLE PERMISOS DE ADMINISTRATIVO
        # tel_admin = Administrativo.objects.filter(ptr_personal_id = telefono_pers.id).first()
        # if tel_admin:
        #     if tel_admin.activo == 1: 
                return "existe_telefono" 
    
    correo_pers = Personal.objects.filter(correo = correo).first()
    if correo_pers: #SI EL CORREO DEL PERSONAL A INGRESAR EXISTIERA (PUEDE QUE SEA UN MECANICO QUE SE LE ASIGNARA TAREAS DE ADMINISTRATIVO), EL ADMINISTRATIVO LOGEADO EN EL SISTEMA DEBERA OTORGARLE PERMISOS DE ADMINISTRATIVO
        # correo_admin = Administrativo.objects.filter(ptr_personal_id = correo_pers.id).first()
        # if correo_admin:
        #     if correo_admin.activo == 1:
                return "existe_correo"

def nombre_usuario(nombre,apellido):
    #SI EXISTE EL USUARIO, AGREGAR NUMERO AL FINAL (EJ. jperez, jperez1, jperez2)
    apellido_unido = apellido.replace(' ','')
    usuario = nombre[0:1:1] + apellido_unido
    cant_usuario = Personal.objects.filter(usuario__contains=usuario).count()
    if cant_usuario > 0: #EXISTE MAS DE UN jperez
        usuario = nombre[0:1:1] + apellido + str(cant_usuario)
    return usuario

def validar_billetes(total_billetes_2000,total_billetes_1000,total_billetes_500,total_billetes_200,total_billetes_100,total_billetes_50,total_billetes_20):
    if total_billetes_2000 < 0:
        error = "Ingrese un valor correcto para los billetes de $2000"
    elif total_billetes_1000 < 0:
        error = "Ingrese un valor correcto para los billetes de $1000"
    elif total_billetes_500 < 0:
        error = "Ingrese un valor correcto para los billetes de $500"
    elif total_billetes_200 < 0:
        error = "Ingrese un valor correcto para los billetes de $200"
    elif total_billetes_100 < 0:
        error = "Ingrese un valor correcto para los billetes de $100"
    elif total_billetes_50 < 0:
        error = "Ingrese un valor correcto para los billetes de $50"
    elif total_billetes_20 < 0:
        error = "Ingrese un valor correcto para los billetes de $20"
    else:
        error = None
    return error

def validar_monedas(total_monedas_50,total_monedas_10,total_monedas_5,total_monedas_2,total_monedas_1):
    if total_monedas_50 < 0:
        error = "Ingrese un valor correcto para las monedas de $50"
    elif total_monedas_10 < 0:
        error = "Ingrese un valor correcto para las monedas de $10"
    elif total_monedas_5 < 0:
        error = "Ingrese un valor correcto para las monedas de $5"
    elif total_monedas_2 < 0:
        error = "Ingrese un valor correcto para las monedas de $2"
    elif total_monedas_1 < 0:
        error = "Ingrese un valor correcto para las monedas de $1"
    else:
        error = None
    return error

def funcion_paginas_varias(req,instancia_model):
    paginator = Paginator(instancia_model, 5)  # 5 motos por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)

    return page_obj

def validar_entrega_menor_precio(moneda_entrega,entrega,elemento,precio_dolar,elemento_tipo,existe_cuota,id_elemento):
    error = None
    if moneda_entrega == "Pesos":             
        if elemento.moneda_precio == "Pesos":
            if int(entrega) > int(elemento.precio):
                error = "El pago no puede exceder el precio total del accesorio"
        else:
            if int(entrega) > int((elemento.precio * precio_dolar)):
                error = "El pago no puede exceder el precio total del accesorio"            
    else:
        if elemento.moneda_precio == "Pesos":
            if int(int(entrega) * precio_dolar) > int(elemento.precio):
                error = "El pago no puede exceder el precio total del accesorio"
        else:
            if int(entrega) > int((elemento.precio * precio_dolar)):
                error = "El pago no puede exceder el precio total del accesorio" 
    
    if existe_cuota:
        if elemento_tipo == "Accesorio":
            cuota = CuotasAccesorios.objects.filter(venta_id=id_elemento).latest('id')
        else:
            cuota = CuotasMoto.objects.filter(venta_id=id_elemento).latest('id')
        
        if moneda_entrega == "Pesos":
            if int(entrega) > int(cuota.cant_restante_pesos):
                error = "El pago no puede exceder el valor restante en pesos"
        else:
            if int(entrega) > int(cuota.cant_restante_dolares):
                error = "El pago no puede exceder el valor restante en dólares"
    
    return error

def obtener_compras_accesorios(req,id_venta):
        resultados_cuotas = (
                CuotasAccesorios.objects
                .filter(venta_id=id_venta)
                .values(
                    'id',
                    'fecha_pago', 
                    'fecha_prox_pago',  
                    'cant_restante_dolares', 
                    'cant_restante_pesos', 
                    'moneda', 
                    'observaciones',
                    'valor_pago_dolares',
                    'valor_pago_pesos',
                    'comprobante_pago'
                )
            )
            
        res_pagos = []
        i = 1
        for resultado in resultados_cuotas:
                    ca = CuotasAccesorios.objects.get(id=resultado['id'])
                    res_pagos.append({
                    'cuota': resultado,
                    'comprobante_pago': ca.comprobante_pago.url if ca.comprobante_pago else None,
                    'mostrar_boton': i == len(resultados_cuotas)           
                    })
                    i = i + 1
        page_obj = funcion_paginas_varias(req,res_pagos)

        return page_obj

def obtener_compras_motos(req,id_cv):
        resultados_cuotas = (
                CuotasMoto.objects
                .filter(venta_id=id_cv)
                .values(
                    'id',
                    'fecha_pago', 
                    'fecha_prox_pago',  
                    'cant_restante_dolares', 
                    'cant_restante_pesos', 
                    'moneda', 
                    'observaciones',
                    'valor_pago_dolares',
                    'valor_pago_pesos',
                    'comprobante_pago'
                )
            )
            
        res_documentacion = []
        i = 1
        for resultado in resultados_cuotas:
                    cm = CuotasMoto.objects.get(id=resultado['id'])
                    res_documentacion.append({
                    'cuota': resultado,
                    'comprobante_pago': cm.comprobante_pago.url if cm.comprobante_pago else None,
                    'mostrar_boton': i == len(resultados_cuotas)           
                    })
                    i = i + 1
        page_obj = funcion_paginas_varias(req,res_documentacion)
        return page_obj

def valores_compras(existe_cuota,moneda,entrega,id_elemento,elemento,elemento_tipo,precio_dolar):
    if not existe_cuota:
        if moneda == "Pesos":
            entrega_pesos = entrega
            entrega_dolares = 0
            if elemento.moneda_precio == "Pesos":
                resto_pesos = int(elemento.precio) - int(entrega_pesos)
                resto_dolares = resto_pesos / precio_dolar
            else:
                resto_pesos = int((elemento.precio * precio_dolar)) - int(entrega_pesos)
                resto_dolares = resto_pesos / precio_dolar                       
        else:
            entrega_pesos = 0
            entrega_dolares = entrega
            if elemento.moneda_precio == "Pesos":
                resto_dolares = int((elemento.precio / precio_dolar)) - int(entrega_dolares)
                resto_pesos = resto_dolares * precio_dolar
            else:
                resto_dolares = int(elemento.precio) - int(entrega_dolares)
                resto_pesos = resto_dolares * precio_dolar 
    else:
        if elemento_tipo == "Accesorio":
            cuota = CuotasAccesorios.objects.filter(venta_id=id_elemento).latest('id')
        else:
            cuota = CuotasMoto.objects.filter(venta_id=id_elemento).latest('id')
        
        if moneda == "Pesos":
            entrega_pesos = entrega
            entrega_dolares = 0
            resto_pesos = int(cuota.cant_restante_pesos) - int(entrega_pesos)
            resto_dolares = resto_pesos / precio_dolar
        else:
            entrega_pesos = 0
            entrega_dolares = entrega
            resto_dolares = int(cuota.cant_restante_dolares) - int(entrega_dolares)
            resto_pesos = resto_dolares * precio_dolar

            #resto_dolares,resto_pesos,entrega_pesos,entrega_dolares
    
    lista = [resto_dolares,resto_pesos,entrega_pesos,entrega_dolares]
    return lista

def obtener_detalles_cuotas_comunes(id_cv):
    compra = ComprasVentas.objects.get(id=id_cv)
    moto = Moto.objects.get(id=compra.moto_id)
    producto = f"{moto.marca} {moto.modelo}"
    primeros_pagos = CuotasMoto.objects.filter(venta_id=id_cv,tipo_pago__in=["Seña", "Entrega inicial","Entrega"]).order_by('-id')
    existen_pagos = CuotasMoto.objects.filter(venta_id=id_cv).first()
    if existen_pagos:
        ultimo_pago_general = CuotasMoto.objects.filter(venta_id=id_cv).latest('id')
        data_p_pagos = []
        for p_p in primeros_pagos:
            data_p_pagos.append({
                "primeros_pagos":p_p,
                "boton_ultimo_pago": True if p_p.id == ultimo_pago_general.id else False
            })
        moneda = "$" if moto.moneda_precio == "Pesos" else "U$S"
        primer_fin = Financiamientos.objects.filter(venta_id=id_cv).order_by('id').first()
        financiamiento = f"{str(primer_fin.cantidad_cuotas)} x {moneda} {str(primer_fin.valor_cuota)}"
    else:
        data_p_pagos = None
        financiamiento = None


    #LISTAR FINANCIAMIENTOS EN SELECT
    financiamientos_select = Financiamientos.objects.filter(venta_id=id_cv,inicial=0).order_by('-id')
    data_financiamientos = []
    for f_s in financiamientos_select:
        fecha_str = f_s.fecha.strftime("%d/%m/%Y")  # Ajusta el formato si es necesario
        actual = "Actual" if f_s.actual else ""
        data_financiamientos.append({
            "financiamientos": f"{fecha_str} {actual}".strip(),  # Quita espacios en blanco si no hay "Actual"
            "id": f_s.id,
        })
    
    data = [
        producto,
        moto.precio,
        moto.precio_final,
        compra.forma_de_pago,
        data_p_pagos,
        financiamiento,
        data_financiamientos,
    ]
    return data

def obtener_detalles_cuotas_financiamiento(req,id_f):
    resultados = (
                CuotasFinanciacion.objects
                .filter(financiamiento_id=id_f)
                .select_related('cuota','financiamiento')
                .values(
                    'cuota__id',
                    'cuota__fecha_pago', 
                    'cuota__fecha_prox_pago',  
                    'cuota__cant_restante_dolares', 
                    'cuota__cant_restante_pesos', 
                    'cuota__moneda', 
                    'cuota__observaciones',
                    'cuota__valor_pago_dolares',
                    'cuota__valor_pago_pesos',
                    'cuota__comprobante_pago',
                    'cuota__tipo_pago',
                    'financiamiento__id'
                ).order_by('-cuota__id')
            )
    res_pagos = []
    f = Financiamientos.objects.get(id=id_f)
    existen_pagos = CuotasMoto.objects.filter(venta_id=f.venta_id).first()
    if existen_pagos:
        ult_cuota = CuotasMoto.objects.filter(venta_id=f.venta_id).latest('id')
        i = 1
        for resultado in resultados:
            ca = CuotasMoto.objects.get(id=resultado['cuota__id'])
            f = Financiamientos.objects.get(id=resultado['financiamiento__id'])
            res_pagos.append({
            'cuota': resultado,
            'comprobante_pago': ca.comprobante_pago.url if ca.comprobante_pago else None,
            # 'mostrar_boton': (i == len(resultados) and f.actual) or (ca.id == ult_cuota.id)  
            'mostrar_boton': (ca.id == ult_cuota.id) and f.actual
            })
            i = i + 1

    page_obj = funcion_paginas_varias(req,res_pagos)
    return page_obj

def crear_certificado_bikeup(cliente,telefono,moto,id_cv):
    output_dir = os.path.join(settings.MEDIA_ROOT, 'certificado_venta')

    # doc.save(docx_file_path)
    # doc = Document('D:\Escritorio\SISTEMA UMPIERREZ MOTOS\cert_bikeup.docx')  # Este es el archivo de Word que quieres editar
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ruta del archivo de plantilla (ajustado para que sea desde media)
    plantilla_path = os.path.join(settings.BASE_DIR, 'media', 'cert_bikeup.docx')
    
    # Crear el documento Word a partir del archivo de plantilla
    doc = Document(plantilla_path)

    locale.setlocale(locale.LC_TIME, 'spanish')
    fecha_actual = datetime.now()
    fecha_formateada = fecha_actual.strftime("%d DE %B").upper()
    longitud_doc = len(cliente.documento)
    doc_num = ""
    apto = "APTO " + str(cliente.num_apartamento) if cliente.num_apartamento > 0 else ""
    direccion = cliente.calle.upper() + " " + str(cliente.numero) + apto + ", " + cliente.ciudad.upper()
    for i in range(2,longitud_doc):
                    doc_num = doc_num + cliente.documento[i]
    if moto.moneda_precio == "Pesos":
        moneda = "PESOS"
    else:
        moneda = "DOLARES"
    for p in doc.paragraphs:
        if 'FECHA_ACTUAL' in p.text:
            p.text = p.text.replace('FECHA_ACTUAL', fecha_formateada)
        if 'NOMBRE_CLIENTE' in p.text:
            p.text = p.text.replace('NOMBRE_CLIENTE', cliente.nombre.upper() + " " + cliente.apellido.upper())
        if 'DOCUMENTO_CLIENTE' in p.text:
            p.text = p.text.replace('DOCUMENTO_CLIENTE', doc_num)
        if 'TELEFONO_CLIENTE' in p.text:
            p.text = p.text.replace('TELEFONO_CLIENTE', telefono)
        if 'DIRECCION_CLIENTE' in p.text:
            p.text = p.text.replace('DIRECCION_CLIENTE', direccion)
        if 'MOTO_MARCA' in p.text:
            p.text = p.text.replace('MOTO_MARCA', moto.marca)
        if 'MOTO_MODELO' in p.text:
            p.text = p.text.replace('MOTO_MODELO', moto.modelo)
        if 'MOTO_CILINDROS' in p.text:
            p.text = p.text.replace('MOTO_CILINDROS', str(moto.num_cilindros))
        if 'MOTO_MOTOR' in p.text:
            p.text = p.text.replace('MOTO_MOTOR', str(moto.motor))
        if 'MOTO_PASAJEROS' in p.text:
            p.text = p.text.replace('MOTO_PASAJEROS', str(moto.cantidad_pasajeros))
        if 'MOTO_ANIO' in p.text:
            p.text = p.text.replace('MOTO_ANIO', str(moto.anio))
        if 'MOTO_NUM_MOTOR' in p.text:
            p.text = p.text.replace('MOTO_NUM_MOTOR', moto.num_motor)
        if 'MOTO_NUM_CHASIS' in p.text:
            p.text = p.text.replace('MOTO_NUM_CHASIS', moto.num_chasis)
        if 'MOTO_MONEDA' in p.text:
            p.text = p.text.replace('MOTO_MONEDA', moneda)
        if 'PRECIO_MOTO' in p.text:
            p.text = p.text.replace('PRECIO_MOTO', str(moto.precio))

    nombre_archivo = f"{moto.id}_{moto.marca}_{moto.modelo}_{cliente.nombre}_{cliente.apellido}_{id_cv}"
    docx_file_path = os.path.join(output_dir, f"{nombre_archivo}.docx")
    doc.save(docx_file_path)

    ruta_archivo = convertir_docx_a_pdf(docx_file_path,nombre_archivo,id_cv)
    if os.path.exists(docx_file_path):
        os.remove(docx_file_path)


def convertir_docx_a_pdf(docx_file_path,nombre_archivo,id_cv):
    # Inicializar COM
    pythoncom.CoInitialize()

    try:
        # Iniciar una instancia de Word
        word = win32com.client.Dispatch("Word.Application")
        
        # Abrir el archivo .docx
        doc = word.Documents.Open(docx_file_path)

        # Asegurarse de que el directorio para guardar el PDF exista
        output_dir = os.path.join(settings.MEDIA_ROOT, 'certificado_venta')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Definir la ruta del archivo PDF de salida
        pdf_file_path = os.path.join(output_dir, f'{nombre_archivo}.pdf')

        # Guardar el documento como .pdf
        doc.SaveAs(pdf_file_path, FileFormat=17)  # El formato 17 corresponde a PDF
        
        # Cerrar el documento y la aplicación de Word
        doc.Close()
        word.Quit()

        # Eliminar el archivo .docx original después de generar el PDF
        if os.path.exists(docx_file_path):
            os.remove(docx_file_path)
            print(f"El archivo .docx '{docx_file_path}' ha sido eliminado.")

        # Devolver la ruta del archivo PDF generado
        compra_venta = ComprasVentas.objects.get(id=id_cv)
    
    # Abrir el archivo PDF y asignarlo al campo certificado_venta
        with open(pdf_file_path, 'rb') as pdf_file:
            compra_venta.certificado_venta.save(f'{nombre_archivo}.pdf', File(pdf_file))
    
    # Guardar los cambios en la base de datos
        compra_venta.save()

        return pdf_file_path

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Finalizar COM (si es necesario)
        pythoncom.CoUninitialize()

def contexto_editar_usuario(req,mensaje_error):
    usuario = req.user
    usuario_actual = Personal.objects.filter(usuario=usuario.username).first()
    f_nac_formateada = usuario_actual.fecha_nacimiento.strftime('%Y-%m-%d')
    tipo_documento_ci = usuario_actual.documento[0:2:1]
    tipo_documento_pas_dni = usuario_actual.documento[0:3:1]

    longitud_doc = len(usuario_actual.documento)
    doc_num = ""
    
    if tipo_documento_ci == "CI":
        #
        tipo_doc = "CI"
        for i in range(2,longitud_doc):
            doc_num = doc_num + usuario_actual.documento[i]
    elif tipo_documento_pas_dni == "DNI":
        tipo_doc = "DNI"
        for i in range(3,longitud_doc):
            doc_num = doc_num + usuario_actual.documento[i]
    else:
        tipo_doc = "PAS"
        for i in range(3,longitud_doc):
            doc_num = doc_num + usuario_actual.documento[i]

    longitud_correo_princ = len(usuario_actual.correo)
    c_p = "" 
    lon = 0
    for i in range(0,longitud_correo_princ):
        if usuario_actual.correo[i] == "@":
            j = i
            break
        else:
            lon += 1
            c_p = c_p + usuario_actual.correo[i]
    
    longitud_dominio = longitud_correo_princ - lon
    dom_princ = ""
    pos = j
    for j in range(pos,longitud_correo_princ):
        dom_princ = dom_princ + usuario_actual.correo[j]
    
    contexto = {"datos":usuario_actual,
                "f_nac":f_nac_formateada,
                "tipo_doc":tipo_doc,
                "doc_num":doc_num,
                "correo":c_p,
                "dom_princ":dom_princ,
                "error_message":mensaje_error if mensaje_error else None}
    return contexto

def json_para_resumen_pagos(moto,id_cv):
    financiaciones = Financiamientos.objects.filter(venta_id=id_cv).order_by('fecha')
    cv = ComprasVentas.objects.get(id=id_cv)
    if financiaciones:
        fin_data = [
                {   
                    "detalle":moto.marca + " " + moto.modelo,
                    "precio_inicial":int((fin.cantidad_cuotas * fin.valor_cuota) - ((fin.cantidad_cuotas * fin.recargo)/100)) ,
                    "precio_final":int(fin.cantidad_cuotas * fin.valor_cuota),
                    "moneda":fin.moneda_cuota,
                    "financiacion":f"{fin.cantidad_cuotas} x {fin.moneda_cuota} {fin.valor_cuota}"
                    # "fecha_vencimiento": cuota.fecha_prox_pago.strftime('%Y-%m-%d'),
                }
                for fin in financiaciones
            ]
        fin_pagos_json = json.dumps(fin_data)
    else:
        fin_pagos_json = None


    primeros_pagos = CuotasMoto.objects.filter(venta_id=id_cv,tipo_pago__in=["Seña", "Entrega inicial","Entrega"]).order_by('-fecha_pago')
    if primeros_pagos:
        p_pagos_data = [
                {   
                    "tipo_pago":cuota.tipo_pago,
                    "fecha":cuota.fecha_pago.strftime('%Y-%m-%d'),
                    "moneda":cuota.moneda,
                    "monto": float(cuota.valor_pago_pesos) if cuota.moneda == "Pesos" else float(cuota.valor_pago_dolares),
                    # "fecha_vencimiento": cuota.fecha_prox_pago.strftime('%Y-%m-%d'),
                }
                for cuota in primeros_pagos
            ]
        primeros_pagos_json = json.dumps(p_pagos_data)
    else:
        primeros_pagos_json = None
    
    cuotas = CuotasMoto.objects.filter(venta_id=id_cv).exclude(tipo_pago__in=["Seña", "Entrega inicial","Entrega"]).order_by('-id')
    # precio = float(precio_dolar.precio_dolar_tienda) if precio_dolar.precio_dolar_tienda else 0
    if cuotas:
        cuotas_data = [
                {  
                    "tipo_pago":cuota.tipo_pago,
                    "fecha":cuota.fecha_pago.strftime('%Y-%m-%d'),
                    "moneda":cuota.moneda,
                    "monto": float(cuota.valor_pago_pesos) if cuota.moneda == "Pesos" else float(cuota.valor_pago_dolares),
                    "fecha_vencimiento": cuota.fecha_prox_pago.strftime('%Y-%m-%d'),
                }
                for cuota in cuotas
            ]
        cuotas_json = json.dumps(cuotas_data)
    else:
        cuotas_json = None
    
    cliente = Cliente.objects.get(id=cv.cliente_id)
    telefono = ClienteTelefono.objects.filter(cliente_id=cv.cliente_id,principal=1).first()
    apto = "Apto " + str(cliente.num_apartamento) if int(cliente.num_apartamento) > 0 else ""
    cliente_data = {
        "cliente": cliente.nombre + " " + cliente.apellido,
        "telefono": telefono.telefono,
        "direccion": cliente.calle + " " + str(cliente.numero) + apto + ", " + cliente.ciudad,
        }
    cliente_json = json.dumps(cliente_data)
    logo = Logos.objects.get(id=1)
    detalle_data={
        "logo_empresa":logo.logo_UM.url,
        "detalle":moto.marca + " " + moto.modelo,
        "precio_inicial":float(moto.precio),
        "precio_final":float(moto.precio_final),
    }
    detalle_json = json.dumps(detalle_data)

    datos = [
        cuotas_json,
        cliente_json,
        detalle_json,
        primeros_pagos_json,
        fin_pagos_json
    ]

    return datos


def funcion_detalles_cuotas(req,id_cv,buscar,id_buscar_f):
    datos = obtener_detalles_cuotas_comunes(id_cv)
    
    
    refinanciaciones = Financiamientos.objects.filter(venta_id=id_cv,inicial = 0).first()
    existen_refinanciaciones = True if refinanciaciones else False #SIRVE PARA MOSTRAR LOS DATOS DE LAS REFINANCIACIONES EN CASO DE QUE EXISTAN
    # mostrar_boton_borrar_financiacion = True if refinanciaciones.actual else False
    if buscar:#SI SE ESTA BUSCANDO UNA REFINANCIACION ESPECIFICA
        page_obj = obtener_detalles_cuotas_financiamiento(req,id_buscar_f)
        financiamiento_buscado = Financiamientos.objects.get(id=id_buscar_f)
        id_f = id_buscar_f
        moneda = "$" if financiamiento_buscado.moneda_cuota == "Pesos" else "U$S" if financiamiento_buscado else None
        financiamiento = f"{str(financiamiento_buscado.cantidad_cuotas)} x {moneda} {str(financiamiento_buscado.valor_cuota)}" if financiamiento_buscado else None
        fecha = financiamiento_buscado.fecha if financiamiento_buscado else None
        mostrar_boton = True if financiamiento_buscado.actual else False
        moneda_pago = financiamiento_buscado.moneda_cuota if financiamiento_buscado else None
        monto_cuota = int(financiamiento_buscado.valor_cuota) if financiamiento_buscado.actual else None
        mostrar_boton_borrar_financiacion = True if financiamiento_buscado.actual else False
    else:
        fin_actual = Financiamientos.objects.filter(venta_id=id_cv,actual=1).first()
        if fin_actual:
            mostrar_boton = True if fin_actual.actual else False
            page_obj = obtener_detalles_cuotas_financiamiento(req,fin_actual.id)
            moneda = "$" if fin_actual.moneda_cuota == "Pesos" else "U$S" if fin_actual else None
            financiamiento = f"{str(fin_actual.cantidad_cuotas)} x {moneda} {str(fin_actual.valor_cuota)}" if fin_actual else None
            fecha = fin_actual.fecha if fin_actual else None
            id_f = fin_actual.id if fin_actual else None
            moneda_pago = fin_actual.moneda_cuota if fin_actual else None
            monto_cuota = int(fin_actual.valor_cuota) if fin_actual else None
            mostrar_boton_borrar_financiacion = True if fin_actual.actual else False
        else:
            #SI NO EXISTE NINGUNA REFINANCIACION NO MUESTRA NADA
            # fins = Financiamientos.objects.filter(venta_id=id_cv,inicial=0).first()
            # #BOTON PAGO REFINANCIAMIENTO
            # mostrar_boton = True if fins.actual else False
            # page_obj = obtener_detalles_cuotas_financiamiento(req,fins.id)
            # moneda = "$" if fins.moneda_cuota == "Pesos" else "U$S" if fins else None
            # financiamiento = f"{str(fins.cantidad_cuotas)} x {moneda} {str(fins.valor_cuota)}" if fins else None
            # fecha = fins.fecha if fins else None
            # id_f = fins.id if fins else None
            
            mostrar_boton = False
            page_obj = False
            moneda = False
            financiamiento = False
            fecha = False
            id_f = False
            moneda_pago = None
            monto_cuota = None
            mostrar_boton_borrar_financiacion = False
    
    

    fin_inicial = Financiamientos.objects.filter(venta_id=id_cv,inicial=1).first()
    # if fin_actual:
    #     moneda = "$" if fin_actual.moneda_cuota == "Pesos" else "U$S"
    #     # fin_json = f"{str(fin_actual.cantidad_cuotas)} x {moneda} {str(fin_actual.valor_cuota)}"
    # elif fin_inicial:
    #     moneda_ini = "$" if fin_inicial.moneda_cuota == "Pesos" else "U$S"
    #     # fin_json = f"{str(fin_inicial.cantidad_cuotas)} x {moneda_ini} {str(fin_inicial.valor_cuota)}"
    # else:
    #     pass
    #     # fin_json = "Sin financiamiento"
    if fin_inicial:
        moneda_ini = "$" if fin_inicial.moneda_cuota == "Pesos" else "U$S"
        fin_ini = f"{str(fin_inicial.cantidad_cuotas)} x {moneda_ini} {str(fin_inicial.valor_cuota)}"

    ult_cuota = CuotasMoto.objects.filter(venta_id=id_cv).first()
    precio_dolar = PrecioDolar.objects.get(id=1)
    
    cv = ComprasVentas.objects.get(id=id_cv)
    moto = Moto.objects.get(id=cv.moto_id)
    if ult_cuota:
        ult_cuota = CuotasMoto.objects.filter(venta_id=id_cv).latest('id')
        cant_restante_pesos = ult_cuota.cant_restante_pesos
        cant_restante_dolares = ult_cuota.cant_restante_dolares
    else:
        
        if moto.moneda_precio == "Pesos":
            cant_restante_pesos = moto.precio_final
            cant_restante_dolares = int(moto.precio_final / precio_dolar.precio_dolar_tienda)
        else:
            cant_restante_pesos = int(moto.precio_final * precio_dolar.precio_dolar_tienda)
            cant_restante_dolares = moto.precio_final

    data_jason = json_para_resumen_pagos(moto,id_cv)
    precio = float(precio_dolar.precio_dolar_tienda) if precio_dolar.precio_dolar_tienda else 0
    contexto = {"id_cv":id_cv,
                "producto":datos[0],
                "precio_inicial":datos[1],
                "precio_final":datos[2],
                "pago_acordado":datos[3],
                "primeros_pagos":datos[4],
                "financiamiento":datos[5],
                "financiamientos":datos[6],
                "page_obj":page_obj,
                "financiacion_info":financiamiento,
                "financiacion_inicial":fin_ini,
                "fecha_financiacion":fecha,
                "boton_pagar":mostrar_boton,
                "fin_actual":existen_refinanciaciones,
                "cant_restante_dolares":int(cant_restante_dolares),
                "cant_restante_pesos":int(cant_restante_pesos),
                "precio_dolar":precio,
                "id_cliente":cv.cliente_id,
                'cuotas_json': data_jason[0],
                'cliente_json': data_jason[1],
                "detalle_json":data_jason[2],
                "p_pagos_json":data_jason[3],
                "id_f":id_f,
                "mon_pago":moneda_pago,
                "fin_pagos_json":data_jason[4],
                "monto_cuota":monto_cuota,
                "mostrar_boton_borrar_financiacion":mostrar_boton_borrar_financiacion}
    # datos = [
    #     cuotas_json,
    #     cliente_json,
    #     detalle_json,
    #     primeros_pagos_json,
    #     fin_pagos_json
    # ]
    
    return contexto