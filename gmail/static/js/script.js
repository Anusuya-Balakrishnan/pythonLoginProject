let btn = document.getElementById("btn");
let usr = document.querySelector(".usr");
// var xhr = new XMLHttpRequest();
btn.addEventListener("click", () => {
  console.log("object");
  usr.style.color = "red";
  //   xhr.open("POST", "http://127.0.0.1:8000/home", true);
  //   xhr.setRequestHeader("Content-Type", "application/json");
  //   xhr.send(
  //     JSON.stringify({
  //       value: "8888888888",
  //     })
  //   );
});
