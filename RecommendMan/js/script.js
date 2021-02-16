var i = 0;
function next(){
    switch(i){
        case 0:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">Hi</div><span>Just now</span></div></div>';
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">How can I help You?</div><span>Just now</span></div></div>';
            break;
        case 1:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">I am looking for a movie to cheer me up. I like will ferrell and comedy.</div><span>Just now</span></div></div>';
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">I found a good movie for you: Elf <img src="https://m.media-amazon.com/images/M/MV5BMzUxNzkzMzQtYjIxZC00NzU0LThkYTQtZjNhNTljMTA1MDA1L2ltYWdlL2ltYWdlXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX182_CR0,0,182,268_AL_.jpg" height = 318 width=" = 200"> </div><span>Just now</span></div></div>';
            break;
        case 2:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">No Christmas movies please</div><span>Just now</span></div></div>';
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">I found a good movie for you: Anchorman <img src="https://m.media-amazon.com/images/M/MV5BMTQ2MzYwMzk5Ml5BMl5BanBnXkFtZTcwOTI4NzUyMw@@._V1_UX182_CR0,0,182,268_AL_.jpg" height = 318 width=" = 200"> </div><span>Just now</span></div></div>';
            break;
        case 3:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">This one looks good. I will watch it!</div><span>Just now</span></div></div>';
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">OK! I have added Anchorman to your Watched list!</div><span>Just now</span></div></div>';
            break;
        case 4:
            document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">I want to watch another movie.</div><span>Just now</span></div></div>';
            break;
        case 5:
            break;
        case 6:
            break;
        case 7:
            break;
    }
    i+=1;
    document.getElementById("chat-input").value = "";
}