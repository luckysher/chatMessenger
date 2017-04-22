//////////////////////////////////////////////////////////
//                                                      //
//  File for handling javascript utility functions      //
//                                                      //
//////////////////////////////////////////////////////////

// Global variables
var scrollInit = false;
var chatdiv = document.getElementById('chatId');
var scrollOffset = 110;
var FRIENDNAME = ""

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue =   decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function getKeyCode(e){
    var code = e.keyCode;
    return code;
}
function getScrollOffset(text){
    if (text.length >= 68){
        var lines = text.length / 68;
        extraOffset = lines * 15;
        newScrollOffset = scrollOffset + extraOffset;
        return newScrollOffset
    }
    return scrollOffset;
}
function curDate(){
  var now = new Date()
  return now.toLocaleFormat('%d-%m-%Y') + " " + now.toLocaleTimeString();
}
function showMessage(message){
    var username = $('#me').text();
    var messListDiv = $('#chatId');
    messListDiv.append('<div class="message"><div class="name name-font"><p><span class="extracted">' + username +
    '</span></p><p><span>' + curDate() + '</span></p></div><div class="message-mine message-font"><div class="spaced"><span >'
     + message + '</span></div></div></div>');
}
function listMessage(message, messageUserDetails){
    var messListDiv = $('#chatId');
    var datetime = new Date(message.messdate);
    var myname = messageUserDetails.me;
    var myid = messageUserDetails.myId;
    var fname = messageUserDetails.fname;
    if (message.chatuser_id == myid){
            messListDiv.append('<div class="message"><div class="name name-font"><p><span class="extracted">' + myname +
    '</span></p><p><span>' + datetime.toLocaleFormat('%d-%m-%Y') + " " + datetime.toLocaleTimeString() + '</span></p></div><div class="message-mine message-font"><div class="spaced"><span >'
     + message.message + '</span></div></div></div>');
     moveScrollbarDown(chatdiv, message.message);
     }else{
        messListDiv.append('<div class="message"><div class="name name-font"><p><span class="extracted">' + fname +
    '</span></p><p><span>' + datetime.toLocaleFormat('%d-%m-%Y') + " " + datetime.toLocaleTimeString() + '</span></p></div><div class="message-your message-font"><div class="spaced"><span >'
     + message.message + '</span></div></div></div>');
     moveScrollbarDown(chatdiv, message.message);
     }
}
function moveScrollbarDown(div, text){
    div.scrollTop += getScrollOffset(text)
}
function sendMessage(e){
   keyCode = getKeyCode(e);
    if (keyCode == 13){
        var txtarea = $('textarea#textarea');
        var message = txtarea.val();
        if(FRIENDNAME == ""){
            alert("Please select a friend ")
         }else{
            if (message.length >= 1){
                //alert("You trying to send message: " + message);
                showMessage(message);
                moveScrollbarDown(chatdiv, message);
                saveMessage(message);
                txtarea.val("");
            }
        }
   }
}
function saveMessage(message){
    var messagesUrl = getMessagesUrl(FRIENDNAME);
    console.log("saving message at : "  + messagesUrl);
   $.ajax({
             method:'POST',
             url:messagesUrl,
             data: { "message" : message }
    }).done(function(mess){
        console.log(JSON.parse(JSON.stringify(mess)).success);
    });
}

function displayMessages(messagesData){
    var messageUserDetails = JSON.parse(JSON.stringify(messagesData[0]));
    var messagesList = messagesData[1];
    var messListDiv = $('#chatId');
    messListDiv.empty();

    for(var i=0; i < messagesList.length; i++){
           var messageData = JSON.parse(JSON.stringify(messagesList[i]));
                listMessage(messageData, messageUserDetails);
           }
}
function showFriends(flist){
              var friendsList = $('#friendslist');
              for(var i=0; i < flist.length; i++){
                    var friend = JSON.parse(JSON.stringify(flist[i]));
                    full_name = friend.first_name + " " + friend.last_name;
                    friendsList.append('<li id=' + friend.id  + ' class="no-select"><span><div class="status off"></div></span><span>' + full_name +'</span></li>');
              }
}