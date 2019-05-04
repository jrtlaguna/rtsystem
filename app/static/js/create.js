function getAttendancePeriod(attendancePeriod) {
  var year = new Date().getFullYear();

  attendancePeriod = attendancePeriod.split('-');
  var first = attendancePeriod[0];
  if(attendancePeriod[1].includes('January')) {
    first = attendancePeriod[0].concat(', ', year - 1);
  }
  var second = attendancePeriod[1].concat(', ', year);
  var finalAttendancePeriod = first.concat(' - ', second);

  return finalAttendancePeriod;
}

function getPayrollPeriod(attendancePeriod) {
  var payrollPeriods = {
    'January': 'February',
    'February': 'March',
    'March': 'April',
    'April': 'May',
    'May': 'June',
    'June': 'July',
    'July': 'August',
    'August': 'September',
    'September': 'October',
    'October': 'November',
    'November': 'December',
    'December': 'January'
  };

  attendancePeriod = attendancePeriod.split('-');
  var secondMonth = attendancePeriod[1].split(' ')[0];
  var payrollMonth = payrollPeriods[secondMonth];
  var year = new Date().getFullYear();
  if(secondMonth == 'December') {
    year += 1;
  }
  var days = getDaysInMonth(year, payrollMonth);

  var finalPayrollPeriod = payrollMonth.concat(' 1 - ', days, ', ', year);

  return finalPayrollPeriod;
}

function getWeeksInMonth(attendancePeriod) {
  attendancePeriod = attendancePeriod.split(' - ');
  var first = attendancePeriod[0];
  var second = attendancePeriod[1];

  var startDate, endDate;
  endDate = new Date(second);

  if( first.includes('December') ) {
    first = first.concat(', ', new Date().getFullYear() + 1);
  } else {
    first = first.concat(', ', new Date().getFullYear());
  }
  startDate = new Date(first);

  var currentDate = startDate;

  var weeksText = [];
  var weeksStartEnd = [];
  while(Number(currentDate) < Number(endDate)) {
    var daysLeft;
    var daysLeftInWeek = 6 - currentDate.getDay();
    var daysLeftInPeriod = getDateDiff(currentDate, endDate);
    if( daysLeftInWeek > daysLeftInPeriod) {
      daysLeft = daysLeftInPeriod;
    } else {
      daysLeft = daysLeftInWeek;
    }

    var end = getNextDate(currentDate, daysLeft);
    if( currentDate.getMonth() == end.getMonth() ) {
      var w = getMonthName(currentDate.getMonth()).concat(' ', currentDate.getDate());
      if(daysLeft > 0) {
        w = w.concat(' - ', end.getDate());
      }
      w = w.concat(', ', end.getFullYear());
      weeksText.push(w);
    } else if( currentDate.getFullYear() == end.getFullYear() ) {
      var w = getMonthName(currentDate.getMonth()).concat(' ', currentDate.getDate(), ' - ', getMonthName(end.getMonth()), ' ', end.getDate(), ', ', end.getFullYear());
      weeksText.push(w);
    } else {
      var w = getMonthName(currentDate.getMonth()).concat(' ', currentDate.getDate(), ', ', currentDate.getFullYear(), ' - ', getMonthName(end.getMonth()), ' ', end.getDate(), ', ', end.getFullYear());
      weeksText.push(w);
    }

    var startFormatted = currentDate.getMonth().toString().concat('/', currentDate.getDate(), '/',currentDate.getFullYear());
    var endFormatted = end.getMonth().toString().concat('/', end.getDate(), '/', end.getFullYear());
    var startEnd = {
      start: startFormatted,
      end: endFormatted
    }
    weeksStartEnd.push(startEnd);
    currentDate = getNextDate(end, 1);
  }

  var data = {
    weeksText: weeksText,
    weeksStartEnd: weeksStartEnd
  }
  return data;
}

function getMonthName(month) {
  var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  return months[month];
}

function getDaysInMonth(year, month) {
  month = getMonthIndex(month);

  return new Date(year, month, 0).getDate();
}

function getNextDate(start, days) {
  var second = 1000;
  var minute = second * 60;
  var hour = minute * 60;
  var day = hour * 24;

  return new Date(Number(start) + (day * days));
}

function getDateDiff(start, end) {
  var second = 1000;
  var minute = second * 60;
  var hour = minute * 60;
  var day = hour * 24;


  return Math.round((end-start)/day);
}
function getMonthIndex(month) {
  var monthIndex = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
  };

  return monthIndex[month]
}

function getStartDate(attendancePeriod) {
  var startDate = attendancePeriod.split('-')[0];
  var year = new Date().getFullYear();

  if(startDate.includes('December')) {
    year--;
  }
  var fullDate = new Date(`${startDate}, ${year}`);
  
  return fullDate;
}

function getEndDate(attendancePeriod) {
  var endDate = attendancePeriod.split('-')[1];
  var year = new Date().getFullYear();
  var fullDate = new Date(`${endDate}, ${year}`);

  return fullDate;
}