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
        setInputBoxPos(`${boxTop}px`, `${boxLeft}px`);
        inputRow = row, inputCol = col;
        showInputBox();
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
    document.getElementById("todoInputInner").style.display = "block";
}

function hideInputBox() {
    document.getElementById("todoInput").style.zIndex = "1";
    document.getElementById("todoInputInner").style.display = "none";
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
            date: displayDate.format().substring(0, 10),
        },
        function (data, status) {
            let parsedData = JSON.parse(data);

            /*
            * filling table with todos
            * */
            firstDay = moment(parsedData[0][0]);
            monthTodo = [];
            for (const day of parsedData) {
                day[0] = moment(day[0]);
                monthTodo.push(day);
                updateDayCell(day);
            }
        });
}

function loadWeek(displayDate) {

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
    switch (dir){
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
