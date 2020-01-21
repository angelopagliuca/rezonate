var canvas, ctx, center_x, center_y, radius, bars,
    x_end, y_end, bar_height, bar_width,
    frequency_array, ctrl, progressCanvas;

bars = 120; //200
bar_width = 6; //2
var songs_json = document.getElementById("songs_div").value;
var songs = JSON.parse(songs_json);  // "original" songs
var shuffled = [...songs];  // shuffled songs

var songList = songs;


function curSongIndex(list_song) {
  return list_song.id === SONG.id;
}

bars = 120; //200
bar_width = 6; //2

SONG = {};
NEXT_INDEX = -1;
CUR_SONG = {};
AUDIO_URL = "";
IMAGE_URL = "";
SONG_TITLE = "";
SONG_ARTIST = "";
SONG_ID = "";
SONG_LYRICS = "";

is_play = false;
is_shuffled = false;
is_repeat = false;

playpause = document.getElementById("play-pause");

function initVisualizer(ele) {
  MEDIA_URL = document.getElementById("media").value;

  info = ele.value.split("[:]");
  AUDIO_URL = info[0];
  IMAGE_URL = info[1];
  SONG_TITLE = info[2];
  SONG_ARTIST = info[3];
  SONG_ID = info[4];
  SONG_LYRICS = info[5];

  // current song
  SONG = {artist:SONG_ARTIST, audio:AUDIO_URL, id:parseInt(SONG_ID), image:IMAGE_URL, lyrics:SONG_LYRICS, title:SONG_TITLE};
  CUR_SONG = {song:SONG, curIndex:songList.findIndex(curSongIndex), ogIndex:songs.findIndex(curSongIndex), shuffledIndex:shuffled.findIndex(curSongIndex)};
  regular();

  playSong();

  startVisualizer();

}

function playSong(){
  if (!is_play) {
    is_play = true;
    playpause.classList.add('fa-pause-circle');
    playpause.classList.remove('fa-play-circle');
  } else {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    audio.pause();
    audio.currentTime = 0;
    playpause.classList.add('fa-pause-circle');
    playpause.classList.remove('fa-play-circle');
  }
}

function startVisualizer(){

    audio = new Audio()
    var context = new (window.AudioContext || window.webkitAudioContext)();
    analyser = context.createAnalyser();

    audio.src = MEDIA_URL + AUDIO_URL; // the source path
    source = context.createMediaElementSource(audio);
    source.connect(analyser);
    analyser.connect(context.destination);

    frequency_array = new Uint8Array(analyser.frequencyBinCount);

    audio.play();
    initProgressBar(audio);
    animationLooper();
}

function initProgressBar(audio){
  var timer;
  var percent = 0;
  audio.addEventListener("playing", function(_event) {
    var duration = _event.target.duration;
    advance(duration, audio);
  });
  audio.addEventListener("pause", function(_event) {
    clearTimeout(timer);
  });
  var advance = function(duration, element) {
    document.getElementById("totalTime").innerHTML = convertElapsedTime(audio.duration);
    var progress = document.getElementById("progress");
    increment = 10/duration
    percent = Math.min(increment * element.currentTime * 10, 100);
    progress.style.width = percent+'%'
    if (Math.floor(element.currentTime) == Math.floor(audio.duration)) {
      next();
    }
    startTimer(duration, element);
  }
  var startTimer = function(duration, element){
    if(percent < 100) {
      timer = setTimeout(function (){advance(duration, element)}, 100);
    }
  }
}

function convertElapsedTime(inputSeconds) {
     var seconds = Math.floor(inputSeconds % 60);
     if (seconds < 10) {
         seconds = "0" + seconds;
     }
     var minutes = Math.floor(inputSeconds/60);
     return minutes + ":" + seconds;
 }

 function toggleLyrics(ele) {
  var lyricText = document.getElementById("lyricText");

  $.ajax({
  url: MEDIA_URL + CUR_SONG.song.lyrics,
  success: function (data){
    lyrics = data.replace(/\n/g, '<br>');

    if (lyricText.innerHTML == "") {
      if (lyrics[0] == "\"") lyrics = lyrics.substring(1, lyrics.length-1)
      lyricText.innerHTML = lyrics;
    } else {
      lyricText.innerHTML = "";
    }
  },
  error: function (xhr, ajaxOptions, thrownError){
    lyricText.innerHTML = "NO LYRICS PROVIDED";
  }
  });
}

 function playOrPause() {
   if (is_play) {
     if (!audio.paused) {
       audio.pause();
       playpause.classList.add('fa-play-circle');
       playpause.classList.remove('fa-pause-circle');
     } else {
       audio.play();
       playpause.classList.add('fa-pause-circle');
       playpause.classList.remove('fa-play-circle');
     }
   }
   return;
 }

// need songs, shuffled, songList, curSong

 function getSong(){
   SONG = songList[index];
   curIndex = index;
   ogIndex = songs.findIndex(curSongIndex);
   shuffledIndex = shuffled.findIndex(curSongIndex);
   return {song:SONG, curIndex:curIndex, ogIndex:ogIndex, shuffledIndex:shuffledIndex};
}

function regular(){
 NEXT_INDEX = 0;
 if (CUR_SONG.curIndex != songList.length-1) {
   NEXT_INDEX = CUR_SONG.curIndex + 1;
 }
}

function toggleShuffle(ele){
  is_shuffled = !is_shuffled;

  if(is_shuffled){
    // shuffles the shuffled list
    shuffled.sort((e1, e2) => Math.random() - Math.random());
    songList = shuffled;
    CUR_SONG.curIndex = CUR_SONG.shuffledIndex;

    $(ele).addClass("active")

  }
  else{
    songList = songs;
    CUR_SONG.curIndex = CUR_SONG.ogIndex;

    $(ele).removeClass("active")

  };
}

function toggleRepeat(ele){
  is_repeat = !is_repeat;

  getNext(ele)
}

function getNext(ele){
  if (is_repeat){
    NEXT_INDEX = CUR_SONG.curIndex;
    $(ele).addClass("active")
  }
  else{
    regular();
    $(ele).removeClass("active")
  }
}

function prev(){
  if(!is_repeat){
    NEXT_INDEX = CUR_SONG.curIndex;
    index = songList.length - 1;
    if (CUR_SONG.curIndex != 0) {
      index = CUR_SONG.curIndex - 1;
    }
    CUR_SONG = getSong(index);
  }
  playSong();
  startVisualizer();
}

function next(){
  if (!is_repeat){
    index = NEXT_INDEX;
    CUR_SONG = getSong(index);
    regular();
  }
  playSong();
  startVisualizer();
}

 function updateBar() {
     canvas.clearRect(0, canvas.height-50, canvas.width, 50);
     canvas.fillRect(0, canvas.height-50, canvas.width, 50);

     var currentTime = audio.currentTime;
     var duration = audio.duration;

     if (currentTime == duration) {
         ctrl.innerHTML = 'Play';
     }

     document.getElementById("currentTime").innerHTML = convertElapsedTime(currentTime);

     var percentage = currentTime / duration;
     var progress = canvas.width * percentage;
     canvas.fillRect(0, canvas.height-50, progress, 50);
 }


 function showImageAndTitle() {
    // set to the size of device
    canvas = document.getElementById("renderer");
    canvas.style.width ='100%';
    canvas.style.height='100%';
    canvas.width  = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    ctx = canvas.getContext("2d");

    // find the center of the window
    center_x = canvas.width / 2;
    center_y = canvas.height / 2 - 75;
    radius = 150;

    ctx.save()
    var img = document.createElement("img");
    img.src = MEDIA_URL + CUR_SONG.song.image; // the source path
    ctx.beginPath();
    ctx.arc(center_x, center_y, radius, 0,  2*Math.PI);
    ctx.clip();
    ctx.drawImage(img, center_x - radius, center_y - radius, radius*2, radius*2);
    ctx.restore()

    // text segment
    ctx.textAlign = "center";
    ctx.fillStyle = "rgb(255, 250, 250)";
    ctx.font = "40px Courier New";
    ctx.fillText(CUR_SONG.song.title, center_x, center_y + 250);
    ctx.font = "25px Courier New";
    ctx.fillText(CUR_SONG.song.artist, center_x, center_y + 300);
 }

 function animationLooper(){
    showImageAndTitle()

    analyser.getByteFrequencyData(frequency_array);
    for(var i = 0; i < bars; i++){

        //divide a circle into equal parts
        rads = Math.PI * 2 / bars;

        bar_height = frequency_array[i]*0.2; //0.4

        // set coordinates
        x = center_x + Math.cos(rads * i) * (radius);
        y = center_y + Math.sin(rads * i) * (radius);
        x_end = center_x + Math.cos(rads * i)*(radius + bar_height + 8);
        y_end = center_y + Math.sin(rads * i)*(radius + bar_height + 8);

        //draw a bar
        drawBar(x, y, x_end, y_end, bar_width,frequency_array[i]);

    }
    window.requestAnimationFrame(animationLooper);
    document.getElementById("currentTime").innerHTML = convertElapsedTime(audio.currentTime);

}

// for drawing a bar
function drawBar(x1, y1, x2, y2, width,frequency){
    var lineColor = "rgb(" + frequency + ", " + 0 + ", " + 255 + ")";

    ctx.strokeStyle = lineColor;
    ctx.lineWidth = width;
    ctx.beginPath();
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2,y2);
    ctx.stroke();
}

function search(input) {
  $.ajax({
  url: MEDIA_URL + CUR_SONG.song.lyrics,
  success: function (data){
    lyrics = data.replace(/\n/g, '<br>');

    if (lyricText.innerHTML == "") {
      if (lyrics[0] == "\"") lyrics = lyrics.substring(1, lyrics.length-1)
      lyricText.innerHTML = lyrics;
    } else {
      lyricText.innerHTML = "";
    }
  },
  error: function (xhr, ajaxOptions, thrownError){
    lyricText.innerHTML = "NO LYRICS PROVIDED";
  }
  });
}
