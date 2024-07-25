// let dataTable;
// let dataTableIsInitialized=false;

// const dataTableOptions={
//     columnDefs:[
//         { className: "centered", targets: [0,1,2,3,4,5,6,7] },
//         { orderable: false, targets:[7] },
//         { searchable: false },

//     ]
// };

// const initDataTable=async()=>{
//     if(dataTableIsInitialized){
//         dataTable.destroy();
//     };

//     await listaRegistrosRecientes();

//     dataTable=$("#datatable-registros").DataTable({});

//     dataTableIsInitialized= true;
// };

const listaRegistrosRecientes=async()=>{
    try{
        const response = await fetch("http://127.0.0.1:8000/lista-registros/");
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
                    <td>${registro.Control == 1
                        ? "<i class='fa-solid fa-check' style='color: green;'></i>"
                        : "<i class='fa-solid fa-xmark' style='color: red;'></i>"}</td>
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