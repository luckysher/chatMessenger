/////////////////////////////////////////////////////////////////////
///                                                               ///
///      Javascript file for handling main chatmess functioning   ///
///      using jquery and utility functions                       ///
///                                                               ///
/////////////////////////////////////////////////////////////////////

// Global variables
var lastFocus = "";
var chatdiv = document.getElementById('chatId');

$(document).ready(function(){
    getFriendsList();
    $('#friendslist li').addClass('no-select');
    initScroll();
});

function initScroll(){
    if (!scrollInit){
        chatdiv.scrollTop  += scrollOffset;
    }
}
function getFriendName(obj){
    var friendName = $(obj).text();
    return friendName;
}

function getMessagesUrl(friendName){
    var url = 'http://127.0.0.1:8000/messages/';
    url = url + friendName + "/";
    return url;
}
function getShowMessagesList(friendName){
    messagesUrl = getMessagesUrl(friendName);
    $.ajax({
                contentType: "application/json",
                type:'GET',
                url:messagesUrl,
                success:function(messageslist){
                 displayMessages(messageslist);
                },
                error:function(){},
    });
}
function getFriendsList(){
     var url = 'http://127.0.0.1:8000/friends/list/';
    $.ajax({
                contentType: "application/json",
                type:'GET',
                url:url,
                success:function(flist){
                                    showFriends(flist);
                                    bindLiClick();
                                },
                error:function(){},
    });
}

function bindLiClick(){
    $('#friendslist li').bind('click',  function(){
    if (lastFocus){
            $(lastFocus).removeClass('friend-selected');
            $(lastFocus).addClass('no-select');
        }
    $(this).removeClass('no-select');
    $(this).addClass('friend-selected');
    lastFocus = $(this);
    var friendName = getFriendName(this);
    FRIENDNAME = friendName;
    getShowMessagesList(friendName);
    });
}