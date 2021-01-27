var i = 0
function next(){
    switch(i){
        case 0:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">Hi</div><span>Just now</span></div></div>';
            break;
        case 1:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">What can I help You?</div><span>Just now</span></div></div>';
            break;
        case 2:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">I am looking for a movie to cheer me up. I like will ferrell and comedy</div><span>Just now</span></div></div>';
            break;
        case 3:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">I found a good movie for you: Elf <img src="img/elf.jpg" height = 318 width=" = 200"> </div><span>Just now</span></div></div>';
            break;
        case 4:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">No Christmas movies please</div><span>Just now</span></div></div>';
            break;
        case 5:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">I found a good movie for you: Anchorman <img src="img/anchorman.jpg" height = 318 width=" = 200"> </div><span>Just now</span></div></div>';
            break;
        case 6:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">This one looks good. I will watch it!</div><span>Just now</span></div></div>';
            break;
        case 7:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">OK! I have added Anchorman to your watched list!</div><span>Just now</span></div></div>';
            break;
    }
    i+=1;
    document.getElementById("chat-input").value = ""
}