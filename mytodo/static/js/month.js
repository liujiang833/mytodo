var monthTodo = []; // store each day's todo in a month
var firstDay;// first day of a month, used as an anchor point to compute index
var inputRow, inputCol;
var displayDate; // controls which month to load
var displayMode;
const MONTH = "month", DAY = "day", WEEK = "week";
const PREV = "prev", NEXT = "next", TODAY = "today";
/*
* ===================================Element behaviors====================================================================*/
$(document).ready(function () {
    /*
    * Load basic data after loading the page*/
    displayDate = moment("2021-07-01");
    displayMode = MONTH;
    loadMonth(displayDate);
    // handler for click events of todo get clicked
    $(".dayTodo").click(function (event) {
        //how to get the selected element:  https://stackoverflow.com/questions/16091823/get-clicked-element-using-jquery-on-event
        showInputBox();
        let id = event.target.id;
        let [row, col, k] = id.match(/[0-9]+/g);
        row = parseInt(row), col = parseInt(col), k = parseInt(k);
        let pInfo = document.getElementById("todoInput").getBoundingClientRect();
        let boxTop = (row * 5 + k) / 25 * pInfo.height;
        let boxLeft = (col + 1) / 7 * pInfo.width;
        let boxHeight = 300, boxWidth = 400;
        if (pInfo.height - boxTop < boxHeight)
            boxTop = pInfo.height - boxHeight;
        if (pInfo.width - boxLeft < boxWidth)
            boxLeft = col / 7 * pInfo.width - boxWidth;
        console.log(row, col, k)
        console.log(boxTop, boxLeft)
        setInputBoxPos(`${boxTop}px`, `${boxLeft}px`);
        inputRow = row, inputCol = col;
    });
    // close inpubox
    $("#todoInput").click(function (event) {
        if (event.target === this) {
            addTodo(inputRow, inputCol);
            document.getElementById("inputTitle").value = "";
            document.getElementById("inputDesc").value = "";
            hideInputBox();
        }

    });
    $("#prevButton").click(function () {
        move(PREV);
    });

    $("#nextButton").click(function () {
        move(NEXT);
    });
    $("#todayButton").click(function () {
        move(TODAY);
    });
    $('#monthButton').click(function () {
        loadMonth(displayDate);
        swtichView("monthView");
    });
});

/* ===================================Helper functions====================================================================*/
function dayDiff(day1, day2) {
    /*
    * source:  https://stackoverflow.com/questions/25150570/get-hours-difference-between-two-dates-in-moment-js
    *  */
    return day2.diff(day1, 'days');
}


function addTodo(row, col) {
    index = row * 7 + col;
    date = monthTodo[index][0].toISOString().slice(0, 10);
    title = document.getElementById("inputTitle").value;
    desc = document.getElementById("inputDesc").value;
    if (title !== "" || desc !== "")
        addTodoUtil(date, title, desc);
}


function addTodoUtil(date, title, description) {
    $.post(
        "/content/add_todo",
        {
            "date": date,
            "title": title,
            "description": description
        }, function (data, status) {
            console.log(data);
        }
    );

}

function setInputBoxPos(top, left) {
    document.getElementById("todoInputInner").style.top = top;
    document.getElementById("todoInputInner").style.left = left;
}

function showInputBox() {
    document.getElementById("todoInput").style.zIndex = "3";
    document.getElementById("todoInput").style.display = "block";
}

function hideInputBox() {
    document.getElementById("todoInput").style.zIndex = "-1";
    document.getElementById("todoInput").style.display = "none";
}

function loadMonth(displayDate) {
    //change month at top left cornor
    document.getElementById("topNavDate").innerHTML = displayDate.format("MMM, YYYY");
    //clear all month data cells
    $(".dayTodo").empty();
    //load and display new ones
    $.post(
        "/content/month",
        {
            date: getDate(displayDate)
        },
        function (data, status) {
            let parsedData = JSON.parse(data);

            /*
            * filling table with todos
            * */
            firstDay = moment(parsedData[0][0]);
            monthTodo = [];
            console.log(parsedData)
            for (const day of parsedData) {
                day[0] = moment(day[0]);
                monthTodo.push(day);
                updateDayCell(day);
            }
        });
}

function loadWeek(displayDate) {
    $.post(
        "/content/week",
        {
            date: getDate(displayDate)
        },
        function (data, status) {
            let parsedData = JSON.parse(data);
            let [notimeTodos, todos] = splitWeekTodos(parsedData);
            updateNotimeTodos(notimeTodos);
            updateTodos(todos);
            swtichView("weekView");
        }
    );

    function splitWeekTodos(parsedData) {
        const DEFUALT_TIME = "00:00:00";
        let notimeTodos = [], todos = [];
        for (const day of parsedData) {
            let dayNotimeTodos = [], dayTodos = [];
            for (const todo of day[1]) {
                if (todo['start'] === DEFUALT_TIME && todo['end'] === DEFUALT_TIME)
                    dayNotimeTodos.push(todo);
                else
                    dayTodos.push(todo);
            }
            notimeTodos.push(dayNotimeTodos);
            todos.push(dayTodos);
        }
        return notimeTodos, todos;
    }

    function updateNotimeTodos(notimeTodos) {

    }

    function updateTodos(todos) {
        todos.forEach((dayTodos, col) => {
            dayTodos.forEach((todo) => {
                const rowStart = getRow(todo['start']);
                const rowEnd = getRow(todo['end'])-1;
                //collapse the rest
                for (let i = rowStart + 1; i <= rowEnd; i++) {
                    document.getElementById("weekTodo-r" + i + "c" + col).style.height = "0";
                }
                //extend firs row
                document.getElementById("weekTodo-r" + rowStart + "c" + col).style.height = (15 * rowEnd - rowStart) + "px";

            });
        });

    }

    function getRow(timeStr) {
        let time = timeStr.split(timeStr, ":");
        let hour = parseInt(time[0]), minute = parseInt(time[1]);
        return hour * 2 + (minute === 30 ? 1 : 0);
    }
}

function loadDay(displayDate) {

}

function updateDayCell(day) {
    /*
    * day:  an array with two elements. The first element is a moment
    *       object that represents the date. The second element is an array
    *       of todos at that day.
    * */
    let dayIndex = dayDiff(firstDay, day[0]);
    let row = parseInt(dayIndex / 7), col = dayIndex % 7;
    document.getElementById(`todo-r${row}c${col}k${0}`).innerHTML = day[0].date();
    //fill with new data
    day[1].forEach((todo, index) => {
        if (index < 4) {
            document.getElementById(`todo-r${row}c${col}k${index + 1}`).innerHTML = todo['title'];
        }
    });
}

function move(dir) {
    switch (displayMode) {
        case MONTH:
            changeDate("month", dir);
            loadMonth(displayDate);
            break;
        case WEEK:
            changeDate("week", dir);
            loadWeek(displayDate);
            break;
        case DAY:
            changeDate("day", dir);
            loadDay(displayDate);
            break;
    }
}

function changeDate(units, dir) {
    switch (dir) {
        case NEXT:
            displayDate = displayDate.startOf(units).add(1, units);
            break;
        case PREV:
            displayDate = displayDate.startOf(units).subtract(1, units);
            break;
        case TODAY:
            displayDate = moment();
    }
}

function swtichView(view) {
    document.getElementById("monthView").style.display = "none";
    document.getElementById("weekView").style.display = "none";


    document.getElementById(view).style.display = "block";
}

function getDate(momentObj) {
    return momentObj.format().substring(0, 10)
}
