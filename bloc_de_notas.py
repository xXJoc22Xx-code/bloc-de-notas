
import streamlit as st
import uuid

#Clases y Funciones

class Nota:
  def __init__(self,titulo,contenido):
    self.id = str(uuid.uuid4())
    self.titulo = titulo
    self.contenido = contenido

  def mostrar(self):
    return f"Titulo: {self.titulo}\nContenido: {self.contenido}"

class NotaTexto(Nota):
  def mostrar(self):
    return f"{self.contenido}"

class NotaLista(Nota):
  def __init__(self,titulo,items):
    contenido= "\n".join(f"-{item}" for item in items)
    super().__init__(titulo,contenido)
    self.items = items

  def mostrar(self):
    return f"\n".join(f"- {item}" for item in self.items)

class NotaImagen(Nota):
  def __init__(self,titulo,url,descripcion=""):
    super().__init__(titulo,descripcion)
    self.url = url
  
  def mostrar(self):
      st.image(self.url, caption=self.titulo, use_container_width=True)
      return f"Descripcion: {self.contenido}"

    

class BlocDeNotas:
  def __init__(self):
    self.notas={}

  def agregar_nota(self,nota):
    self.notas[nota.id] = nota

  def obtener_notas(self):
    return list(self.notas.values())

  def buscar_nota(self,titulo):
    return[nota for nota in self.notas.values() if titulo.lower() in nota.titulo.lower()]

  def eliminar_nota(self,id_nota):
    if id_nota in self.notas:
      del self.notas[id_nota]
      return True
    return False

  #Main

def main():
    st.title("====Bloc De Notas====")

    if'bloc' not in st.session_state:
      st.session_state.bloc = BlocDeNotas()

    st.sidebar.header("Menu")
    opcion = st.sidebar.selectbox(
        "Seleccione una opcion",
        ["Crear Nota","Mostrar Notas","Buscar Nota", "Eliminar Nota"]
    )
    #Opcion 1
    if opcion == "Crear Nota":
      st.header("Crear Nueva Nota")
      tipo_nota = st.selectbox("Tipo de nota: ",["Texto","Lista","Imagen"])
      titulo = st.text_input("Titulo de la nota*")

      if tipo_nota == "Texto":
        contenido = st.text_area("Contenido de la nota")
        if st.button("Guardar Nota de Texto") and titulo:
          st.session_state.bloc.agregar_nota(NotaTexto(titulo,contenido))
          st.success("Nota de Texto agregada con exito!")

      elif tipo_nota == "Lista":
        items_text = st.text_area("Elementos de la lista (elemento/linea )")
        items = [item.strip() for item in items_text.split('\n') if item.strip()]
        if st.button("Guardar Nota de Lista") and titulo and items:
          st.session_state.bloc.agregar_nota(NotaLista(titulo,items))
          st.success("Nota de Lista agregada con exito!")

      elif tipo_nota == "Imagen":
        url = st.text_input("URL de la imagen (Ejemplo: https://ejemplo.com/imagen.jpg): ")
        descripcion = st.text_area("Descripcion de la imagen")
        if st.button("Guardar Nota de Imagen") and titulo and url:
          st.session_state.bloc.agregar_nota(NotaImagen(titulo,url,descripcion))
          st.success("Nota de Imagen agregada con exito!")
    #Opcion 2
    elif opcion == "Mostrar Notas":
      st.header("Todas las notas")
      notas = st.session_state.bloc.obtener_notas()

      if not notas:
        st.info("No hay notas aun")
      else:
        for nota in notas:
          st.subheader(nota.titulo)
          if isinstance(nota, NotaImagen):
            st.write(nota.contenido)
            nota.mostrar()
          else:
            st.write(nota.mostrar())
          st.write("---")
    #Opcion 3
    elif opcion == "Buscar Nota":
      st.header("Buscar Nota por titulo")
      busqueda = st.text_input("Ingrese parte del titulo para buscar")

      if st.button("Buscar Notas"):
        if busqueda:
          resultados = st.session_state.bloc.buscar_nota(busqueda)
          if resultados:
            st.success(f"Se encontraron {len(resultados)} notas: ")
            for nota in resultados:
              st.subheader(nota.titulo)
              if isinstance(nota, NotaImagen):
                st.write(nota.contenido)
                nota.mostrar()
              else:
                st.write(nota.mostrar())
              st.write("---")
          else:
            st.warning("No se encontraron notas con ese titulo")
        else:
          st.warning("Por favor ingrese un termino de busqueda")

    #Opcion 4
    elif opcion == "Eliminar Nota":
      st.header("Eliminar Nota")
      notas = st.session_state.bloc.obtener_notas()

      if notas:
        nota_a_eliminar = st.selectbox(
            "Seleccione una nota para eliminar",
            options=notas,
            format_func=lambda nota: nota.titulo
        )

        if st.button("Eliminar Nota Seleccionada"):
          if st.session_state.bloc.eliminar_nota(nota_a_eliminar.id):
            st.success(f"Nota '{nota_a_eliminar.titulo}' eliminada con exito!")
            st.rerun()
          else:
            st.error("Error al eliminar la nota")
      else:
        st.info("No hay notas para eliminar")

if __name__ == "__main__":
  main()
