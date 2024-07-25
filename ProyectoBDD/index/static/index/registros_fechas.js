const listaRegistrosRecientes=async()=>{
    try{
        const response = await fetch("http://127.0.0.1:8000/lista-registro-fechas/");
        const data = await response.json();

        let content = ``; 
        data.data.forEach((registro, index)=>{
            content+= `
                <tr>
                    <td>${registro.id}</td>
                    <td>${registro.Piscina}</td>
                    <td>${registro.Oxigeno}</td>
                    <td>${registro.Ph}</td>
                    <td>${registro.Salinidad}</td>
                    <td>${registro.Fecha}</td>
                    <td>${registro.Hora}</td>
                    <td>
                        <div class="opciones">
                            <a href="actualizar/${registro.id}" class="actualizar">Actualizar</a>
                            <a href="eliminar-registro/${registro.id}"" class="eliminar">Eliminar</a>
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