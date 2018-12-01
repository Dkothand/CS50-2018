$(document).ready(function(){
    var $calendar = $('#calendar').fullCalendar( {

            // Set theme to Bootstrap4 and disable FontAwesome buttons
            themeSystem: 'bootstrap4',
            bootstrapFontAwesome: false,

            // Calendar header options
            header:{
                left: 'prev,next today',
                center: 'title',
                right: 'month,agendaDay,agendaWeek'
            },

            // Allow 'more' link when too many events
            eventLimit: true,

            // Show only weeks for current month
            fixedWeekCount: false,

            // Make calendar respond to clicks and selections
            selectable: true,

            // Enable event edits globally
            editable: true,

// Get events as function using GET request to return JSON object from database
            events: function(start, end, timezone, callback) {
                $.get({
                    url: '/_events',
                    dataType: 'json',
                    data: {
                        start: start.unix(),
                        end: end.unix()
                    },
                    success: function(doc) {

                        var events = [];

                        $(doc).each(function() {
                            events.push(this);
                        });

                        callback(events);

                    }

                });

            },

// Callback when click or drag, creating an event
            select: function(start, end, jsEvent, view) {

                // Format for start/end time display
                starttime = $.fullCalendar.moment(start).format('dddd, h:mm');
                endtime = $.fullCalendar.moment(end).format('dddd, MMMM Do YYYY, h:mm');

                // String for event duration display
                var eventtime = starttime + ' - ' + endtime;
                start = moment(start).format();
                end = moment(end).format();

// Clears text input field of modal before showing modal
// https://stackoverflow.com/questions/21151044/how-to-clear-all-input-fields-in-bootstrap-modal-when-clicking-data-dismiss-butt
                $('#selectModal').on('hidden.bs.modal', function(e) {
                    $(this).find("input,textarea,select").val('').end();
                });

                // Formatting modal for creating event
                $('#startTime').val(start); // Saved to hidden div
                $('#endTime').val(end); // Saved to hidden div
                $('#eventTime').text(eventtime);

                // Displaying modal on calendar date selection
                $('#selectModal').modal('toggle');

                // Whatever happens, unselect selection (Removes highlight on selected calendar cells)
                $calendar.fullCalendar("unselect");

            },// End of select callback options

// Callback triggered when event is clicked; rename or remove event
            eventClick: function(event, jsEvent, view) {

                // Clears text input field of modal before showing modal
                $('#eventModal').on('hidden.bs.modal', function(e) {
                    $(this).find("input,textarea,select").val('').end();
                });

                // Current event title passed to modal
                $('#eventModal #modalTitle').html(event.title);

                // Id given when event was created passed to hidden div
                $('#eventId').val(event.id);
                $('#eventModal').modal();

                // If "Save Changes" button is clicked, renames event
                $('#updateEvent').click(function() {

                    var newTitle = $('#eventName').val();

                    // Check that input field is not empty before pushing update
                    if (newTitle != ""){

                        event.title = newTitle;

                        var data = {
                            title: newTitle,
                            id: event.id
                        };

                    // Updates event title in database
                        $.ajax({
                           url: '/_update',
                           data: data,
                           type: 'POST',
                           success: function(event) {
                               alert("Title changed to " + event.title);
                           }
                        });

                        $('#eventModal').modal('hide');

                        $calendar.fullCalendar("updateEvent", event);
                    }
                });// End of updateEvent functions
            },

// Callback triggered when event is dropped to new location on calendar
            eventDrop: function(event, delta){

                // Insert new start and end times in data to be sent
                var passDrop = {
                    id: event.id,
                    title: event.title,
                    start: moment(event.start).format(),
                    end: moment(event.end).format()
                };

                $.ajax({
                   url: '/_drop',
                   data: passDrop,
                   type: 'POST',
                   success: function(event) {
                       alert(event.title + " moved!");
                   }
                });
            },

// Callback triggered when event is resized on calendar
            eventResize: function(event){

                // Insert new start and end times in data to be sent
                var passDrop = {
                    id: event.id,
                    title: event.title,
                    start: moment(event.start).format(),
                    end: moment(event.end).format()
                };

                $.ajax({
                   url: '/_drop',
                   data: passDrop,
                   type: 'POST',
                   success: function(event) {
                       alert(event.title + " resized!");
                   }
                });
            }
        }); // End of calendar options

// If 'Create' button is clicked in modal
    $('#selectCreate').click(function(){

        // Hide modal
        $('#selectModal').modal('hide');

        // Check event title is not blank
        if ($('#selectName').val() != "") {

            // Create event object from modal data
            var event = {
                title: $('#selectName').val(),
                start: $('#startTime').val(),
                end: $('#endTime').val()
            };

            // Update database with new event; push event to calendar upon success
            $.ajax({
               url: '/_create',
               data: event,
               type: 'POST',
               success: function(event){
                   $calendar.fullCalendar('renderEvent', event, true);
               }
            });
        }
    });

// If 'Remove Event' button is clicked in modal
    $('#removeEvent').click(function(e){

        // Hide modal
        $('#eventModal').modal('hide');

        // Get event's id
        var event = {
            id: $('#eventId').val()
        };

        // Remove event from database; push calendar change upon success
        $.ajax({
           url: '/_remove',
           data: event,
           type: 'POST',
           success: function(event){
               $calendar.fullCalendar('removeEvents', event.id);
           }
        });
    });
});
