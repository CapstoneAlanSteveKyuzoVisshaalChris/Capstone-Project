
var ws=new WebSocket('ws://127.0.0.1:10083');
function send(){
    if(document.getElementById("chat-input").value){
        var date = new Date();
        document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">'+ document.getElementById("chat-input").value +'</div><span>'+date+'</span></div></div>';
        if(ws){
             ws.send(document.getElementById("chat-input").value);
        }
         ws.onmessage=function(evt){
             console.log("fdsa");
             document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">'+evt.data +'</div><span>'+date+'</span></div></div>';
        };
    }else{
        alert("Empty message is not allowed!");
    }
    document.getElementById("chat-input").value = "";
}

function statesend() {
    if (typeof (Storage) !== "undefined") {
        if (sessionStorage.state) {
            sessionStorage.state = 'eyJzZXNzaW9uX2lkIjoiNjc3OGFmYzUtNjExYi00ODQzLWIxMTgtMWRjNjMzZWZiMDg3Iiwic2tpbGxfcmVmZXJlbmNlIjoibWFpbiBza2lsbCIsImFzc2lzdGFudF9pZCI6IjIxMjBkNGI0LTVkMjEtNDg4MC05ODFjLTI0NTQzNmM3ZTEyZiIsImluaXRpYWxpemVkIjp0cnVlLCJkaWFsb2dfc3RhY2siOlt7ImRpYWxvZ19ub2RlIjoiV2VsY29tZSJ9XSwiX25vZGVfb3V0cHV0X21hcCI6eyJXZWxjb21lIjp7IjAiOlswLDBdfX0sImxhc3RfYnJhbmNoX25vZGUiOiJXZWxjb21lIn0=';
        } else {
            sessionStorage.state = 'eyJzZXNzaW9uX2lkIjoiNjc3OGFmYzUtNjExYi00ODQzLWIxMTgtMWRjNjMzZWZiMDg3Iiwic2tpbGxfcmVmZXJlbmNlIjoibWFpbiBza2lsbCIsImFzc2lzdGFudF9pZCI6IjIxMjBkNGI0LTVkMjEtNDg4MC05ODFjLTI0NTQzNmM3ZTEyZiIsImluaXRpYWxpemVkIjp0cnVlLCJkaWFsb2dfc3RhY2siOlt7ImRpYWxvZ19ub2RlIjoiV2VsY29tZSJ9XSwiX25vZGVfb3V0cHV0X21hcCI6eyJXZWxjb21lIjp7IjAiOlswLDBdfX0sImxhc3RfYnJhbmNoX25vZGUiOiJXZWxjb21lIn0=';
        }
        //document.getElementById("result").innerHTML = "You have clicked the button " + sessionStorage.clickcount + " time(s) in this session.";
    } else {
        document.getElementById("result").innerHTML = "Sorry, your browser does not support web storage...";
    }
}