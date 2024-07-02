function fetchTasks() {
    $.ajax({
        url: '/get_tasks/',
        method: 'GET',
        success: function(data) {
            const taskDashboard = $('#task-table-body');
            data.tasks.forEach(function(task) {
                let taskInput = document.getElementById(`task_id_${task.id}`);
                
                if (taskInput) {
                    console.log("Esto si existe, nose que logica poner aqui, jaja xd")
                } else {
                    taskDashboard.empty(); // Clear the dashboard
                    console.log('Borro la tabla papa y actualizo esta caga')
                    updateTable(data)
                }
            });


        },
        error: function(xhr, status, error) {
            console.error('Error fetching tasks:', error);
        }
    });
}

// Fetch tasks every 5 seconds
setInterval(fetchTasks, 5000);

// Initial fetch
fetchTasks();

function updateTable(data){
    const taskDashboard = $('#task-table-body');
    data.tasks.forEach(function(task) {
        // Crear fila de la tabla
        const row = $('<tr>');
        row.append($('<td>').text(task.user__first_name));
        row.append($('<td>').text(task.subject));

        const answerTd = $('<td>');

        const form = $('<form>').attr({method: 'POST', class: 'row'});
        const divCol10 = $('<div>').addClass('col-10');
        const inputAnswer = $('<input>').attr({type: 'text', class: 'form-control', name: 'answer', value: task.answer});
        const inputTaskId = $('<input>').attr({
            type: 'hidden', 
            id: `task_id_${task.id}`, 
            name: 'task_id', 
            value: task.id,
            readonly: task.answer === null ? 'readonly' : undefined
        });

        divCol10.append(inputAnswer, inputTaskId);
        const divCol2 = $('<div>').addClass('col-2');
        const submitBtn = $('<button>').attr({type: 'submit',class: 'btn btn-primary',}).text('Submit');
        divCol2.append(submitBtn);

        form.append(divCol10, divCol2);
        answerTd.append(form);
        row.append(answerTd);

        // Agregar fila a la tabla
        taskDashboard.append(row);
    });
}