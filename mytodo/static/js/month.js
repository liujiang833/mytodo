var todoMap = {};

$(document).ready(function () {
    $.post(
        "/content/range",
        {
            start_date: "2021-07-01",
            end_date: "2021-07-15"
        },
        function (data, status) {
            let parsedData = JSON.parse(data);

            /*
            * filling table with todos
            * */
            console.log(parsedData)
            for (const [dayIndex, day] of parsedData.entries()) {
                window.todoMap[day[0]] = day[1];
                const startIndex = dayIndex * 5;
                document.getElementById("todo"+startIndex).innerHTML = day[0]
                day[1].map((todo, index) =>{
                   if(index < 4){
                       console.log(startIndex+index+1, todo);
                       document.getElementById("todo" + (startIndex+index+1)).innerHTML = todo['title'];
                   }
                });
            }

        });
});

