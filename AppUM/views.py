from django.shortcuts import render
from .models import *
from .utils import crear_pdf
from django.http import HttpResponse
from django.core.files.base import ContentFile
from datetime import datetime
from django.core.paginator import Paginator
from django.shortcuts import render
# Create your views here.

##VISTA DEL LOGIN AL ENTRAR AL SITIO##

def vista_login(req):
    return render(req,"login/login.html",{})

##VALIDACION DE USUARIO Y CONTRASEÑA##
def validacion_login(req):
    try:
        usuario = req.GET['usuario_login']
        passw = req.GET['pass_login']

        usuario_consulta = Personal.objects.filter(usuario=usuario,contrasena=passw).first()
    

        if usuario_consulta:
            mecanico = Mecanico.objects.filter(personal_ptr_id=usuario_consulta.id).first()
            if mecanico:
                if mecanico.activo == 1:
                    existe_mecanico = 1
                    if mecanico.jefe == 1:
                        mecanico_jefe = 1
                    else:
                        mecanico_jefe = 0
                else:
                    existe_mecanico = 0
            else:
                mecanico_jefe = 0
                existe_mecanico = 0
                
            administrativo = Administrativo.objects.filter(personal_ptr_id=usuario_consulta.id).first()
            if administrativo:
                if administrativo.activo == 1:
                    existe_administrativo = 1
                else:
                    existe_administrativo = 0
            else:
                existe_administrativo = 0
        
            if existe_mecanico == 1 and mecanico_jefe == 1 and existe_administrativo == 1:
                renderizar_en = "login/login.html"
                contexto = "Administrativo y Mecanico Jefe"
            elif existe_mecanico == 1 and mecanico_jefe == 0 and existe_administrativo == 1:
                renderizar_en = "login/login.html"
                contexto = "Administrativo y Mecanico Empleado"
            elif existe_administrativo == 1 and existe_mecanico == 0:
                renderizar_en = "perfil_administrativo/padre_perfil_administrativo.html"
                contexto = {"existe_mecanico":0,"mecanico_jefe":0,"existe_administrativo":1}
            elif existe_administrativo == 0 and existe_mecanico == 1 and mecanico_jefe == 1:
                renderizar_en = "login/login.html"
                contexto = "Solo Mecanico Jefe"
            elif existe_administrativo == 0 and existe_mecanico == 1 and mecanico_jefe == 0:
                renderizar_en = "login/login.html"
                contexto = "Solo Mecanico Empleado" 
            else:
                renderizar_en = "login/login.html"
                contexto = "Este usuario fue dado de baja, contactese con el administrador del sistema."
           
        else:
            renderizar_en = "login/login.html"
            contexto = {"resultado":"Error de usuario y/o contraseña"}

    except:
        renderizar_en = "login/login.html"
        contexto = "Algo salió mal"
    #print(existe_mecanico)
    return render(req,renderizar_en,contexto)


def vista_inventario_motos(req):
    motos = Moto.objects.filter(pertenece_tienda=1)

    logo_um = Logos.objects.get(id=1)

    paginator = Paginator(motos, 5)  # 10 motos por página

    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos,"logo_um":logo_um.logo_UM.url if logo_um.logo_UM else None})


def vista_inventario_accesorios(req):
    return render(req,"perfil_administrativo/accesorios/accesorios.html",{})

# def existe_matricula_moto_tienda(matr):
#     existe_moto = Moto.objects.filter(matricula = matr).first()

#     if existe_moto.pertenece_tienda == 0:
#         return "update"
#     else:
#         return "existe_matr"

# def existe_num_motor_moto_tienda(num_motor):
#     existe_moto = Moto.objects.filter(num_motor = num_motor).first()
    
#     if existe_moto.pertenece_tienda == 0:
#         return "update_pert_tienda"
#     else:
#         return "existe_num_motor"

# def existe_num_chasis_moto_tienda(num_motor):
#     existe_moto = Moto.objects.filter(num_motor = num_motor).first()
    
#     if existe_moto.pertenece_tienda == 0:
#         return "update_pert_tienda"
#     else:
#         return "existe_num_motor"

def datos_moto(num_motor, num_chasis):
    existe_num_motor = Moto.objects.filter(num_motor = num_motor).first()
    existe_num_chasis = Moto.objects.filter(num_chasis = num_chasis).first() 
    existen_ambos = Moto.objects.filter(num_motor = num_motor, num_chasis = num_chasis).first() 

    if existe_num_motor:
        if existe_num_motor.pertenece_tienda == 1:
            return "existe_num_motor"
    
    if existe_num_chasis:
        if existe_num_chasis.pertenece_tienda == 1:
            return "existe_num_chasis"
    
    if existen_ambos:
        if existen_ambos.pertenece_tienda == 0:
            return "update_pert_tienda_a_1"

def matricula(matricula,num_motor,num_chasis):
    moto = Moto.objects.filter(num_motor = num_motor, num_chasis = num_chasis).first()
    existe_matricula = Matriculas.objects.filter(matricula = matricula).first()
    if existe_matricula:
        if existe_matricula.activo == 1:
            return "matricula_existe"
        else:
            return "update_activo"
    else:
        return "ingresar_matr"

      


def form_alta_moto(req):
    try:
        if req.method == "POST":
            marca = req.POST['marca_moto'].upper()
            modelo = req.POST['modelo_moto'].upper()
            color = req.POST['color_moto'].upper()
            matricula_mayus = req.POST['matricula_letras'].upper()
            matricula = matricula_mayus + str(req.POST['matricula_numeros'])
            num_motor = req.POST['num_motor_moto'].upper()
            num_chasis = req.POST['num_chasis_moto'].upper()
            
            
            valid_moto = datos_moto(num_motor,num_chasis)
            # print(req.POST['estado_moto'])
            estado_moto = req.POST['estado_moto']
            
            if valid_moto == "existe_num_motor":
                print("YA EXISTE UNA MOTO CON ESE NUMERO DE MOTOR")
            elif valid_moto == "existe_num_chasis":
                print("YA EXISTE UNA MOTO CON ESE NUMERO DE CHASIS")
            else:
                if estado_moto == "nueva":
                    nueva_moto = Moto(marca = marca,
                            modelo = modelo,
                            anio = req.POST['anio_moto'],
                            estado = "Nueva",
                            motor = req.POST['motor_moto'],
			                kilometros = 0,
                            precio = req.POST['precio_moto'],
                            color = color,
                            num_motor = num_motor,
                            num_chasis = num_chasis,
                            pertenece_tienda = 1,
                            pertenece_taller = 0
                            )
                    nueva_moto.save()
                    #pdf = crear_pdf('perfil_administrativo/motos/identificacion_moto.html', {"mensaje":"mensaje de prueba",})
                    logo_um = Logos.objects.get(id=1)
                    logo_um_url = req.build_absolute_uri(logo_um.logo_UM.url) if logo_um.logo_UM else None
                    pdf = crear_pdf('perfil_administrativo/motos/identificacion_moto.html', {
    "moto": {
        "id":nueva_moto.id,
        "marca": nueva_moto.marca,
        "modelo": nueva_moto.modelo,
        "motor": nueva_moto.motor,
        "anio": nueva_moto.anio,
        "kilometros": nueva_moto.kilometros,
        "precio": nueva_moto.precio
    },
    "current_year": datetime.now().year,
      "logo_um": logo_um_url  # Asegúrate de importar datetime
})              
                    if pdf:
                        pdf_file = ContentFile(pdf.content)
                        file_name = f"identificacion_{nueva_moto.id}.pdf"
                # Asignar el archivo al campo identificacion_pdf de la moto
                        nueva_moto.identificacion_pdf.save(file_name, pdf_file)
                        nueva_moto.save()
                    
                    #return render(req,"perfil_administrativo/motos/motos.html",{"motos":motos,"messages":"Moto ingresada con éxito"})

                    contexto = {
                        "messages":"Moto ingresada con éxito. A continuación se visualiza el PDF generado para identificar fisicamente la misma.",
                        'pdf_url': nueva_moto.identificacion_pdf.url,
                        "logo_um":logo_um.logo_UM.url if logo_um.logo_UM else None
                        
                    }
                    return render(req,"perfil_administrativo/motos/contenido_pdf.html",contexto)
                    #return HttpResponse(pdf, content_type='application/pdf')
                else:
                    #INGRESAR MOTOS USADAS
                    pass

            return render(req,"perfil_administrativo/motos/alta_moto.html",{})
        else:
            return render(req,"perfil_administrativo/motos/alta_moto.html",{})
    
    except:
        return render(req,"perfil_administrativo/motos/alta_moto.html",{"mensaje":"Algo salió mal"})


def baja_moto(req,id_moto):
    if req.method == 'POST':

      motoDel = Moto.objects.get(id=id_moto)
      motoDel.pertenece_tienda = 0
      motoDel.save()
      return render(req, "perfil_administrativo/motos/baja_moto.html", {"message":"Moto borrada con éxito","id_moto":0})
      #return HttpResponse(f"<p>{id_auto}</p>")
    else:
       #print(f"Id auto es: {id_auto}")
       return render(req, "perfil_administrativo/motos/baja_moto.html", {"id_moto":id_moto})
       #return HttpResponse(f"<p>{id_auto}</p>")

def busqueda_marca(req):
    marca = req.GET.get('marca')
    #if req.method == 'get':
    motos = Moto.objects.filter(marca__icontains=marca,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_modelo(req):
    modelo = req.GET.get('modelo')
    #if req.method == 'get':
    motos = Moto.objects.filter(modelo__icontains=modelo,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_marca_modelo(req):
    marca = req.GET.get('marca_modelo')
    modelo = req.GET.get('modelo_marca')
    #if req.method == 'get':
    motos = Moto.objects.filter(marca__icontains=marca,modelo__icontains=modelo,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_anio(req):
    anio = req.GET.get('anio')
    
    #if req.method == 'get':
    motos = Moto.objects.filter(anio=anio,pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_kms(req):
    km_minimo = req.GET.get('km_minimo')
    km_maximo = req.GET.get('km_maximo')
    #if req.method == 'get':
    motos = Moto.objects.filter(kilometros__range=(km_minimo, km_maximo),pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})

def busqueda_precio(req):
    precio_minimo = req.GET.get('precio_minimo')
    precio_maximo = req.GET.get('precio_maximo')
    #if req.method == 'get':
    motos = Moto.objects.filter(precio__range=(precio_minimo, precio_maximo),pertenece_tienda=1)
    paginator = Paginator(motos, 5)  # 10 motos por página
    page_number = req.GET.get('page')  # Obtiene el número de página desde la URL
    page_obj = paginator.get_page(page_number)  # Obtiene la página solicitada

    return render(req,"perfil_administrativo/motos/motos.html",{'page_obj': page_obj,"motos":motos})