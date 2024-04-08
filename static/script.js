const playButton = document.querySelector('.playButton');
const audioPlayer = document.querySelector('.audioPlayer');
const audioData = "blob:https://www.youtube.com/1b987a8e-946b-4234-aec3-cab2dae52624"

// Create a Blob from the audio data
const blob = new Blob([audioData], { type: 'audio/mp3' });

// Create a Blob URL
const blobUrl = "blob:https://www.youtube.com/1b987a8e-946b-4234-aec3-cab2dae52624"

// Set the Blob URL as the audio source
audioPlayer.src = blobUrl;

console.log(playButton)

// Play the audio
function playSound() {
  console.log("hshshsh")
  audioPlayer.play();
}

let isPlaying = false;

playButton.addEventListener('click', () => {
  if (isPlaying) {
    audioPlayer.pause();
    console.log("tat")
  } else {
    playSound()
    console.log("bat");
  }
  isPlaying = !isPlaying;
});