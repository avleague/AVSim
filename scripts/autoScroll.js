const messages = document.getElementById('cmdText');

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

$("#cmdText").on('scroll', function(){
  scrolled=true;
});

//scrollToBottom();

setInterval(getMessages, 100);
