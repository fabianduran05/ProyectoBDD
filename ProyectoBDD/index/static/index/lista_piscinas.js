const listaRegistrosRecientes=async()=>{
    try{
        const response = await fetch("http://127.0.0.1:8000/piscinas-todas/");
        const data = await response.json();

        let content = ``; 
        data.data.forEach((registro, index)=>{
            content+= `
                <tr>
                    <td>${registro.id}</td>
                    <td>${registro.Nombre}</td>
                    <td>${registro.Ubicacion}</td>
                    <td>
                        <div class="opciones">
                            <a href="actualizar-piscina/${registro.id}" class="actualizar">Actualizar</a>
                            <a href="eliminar-piscina/${registro.id}" class="eliminar">Eliminar</a>
                        </div>  
                    </td>
                </tr>
            `;
        });
        table_registro.innerHTML = content;
    }catch(ex){
        alert(ex);
    }
};

window.addEventListener('load', async()=>{
    await listaRegistrosRecientes();
});