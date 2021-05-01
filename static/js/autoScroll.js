const messages = document.getElementById('cmd-text');

var scrolled = false;

function runGetMessages(){
  scrolled = false;
  getMessages();
}

function getMessages() {
  shouldScroll = messages.scrollTop + messages.clientHeight === messages.scrollHeight;

  if (!shouldScroll) {
    scrollToBottom();
  }

}

function scrollToBottom() {
  if(!scrolled){
    messages.scrollTop = messages.scrollHeight;
  }
}

$("#cmd-text").on('scroll', function(){
  scrolled=true;
});

//scrollToBottom();

setInterval(getMessages, 100);