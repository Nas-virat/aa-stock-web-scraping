var timesClicked = 0;
var index = '00001';

function getindex(){
    fetch('filter-HK-CODE2.csv.json')
    .then(response => response.json())
    .then(data => {
        //console.log(data["StockCode"][timesClicked]);
        index = data["StockCode"][timesClicked];
    })
}


function setImage(image) {
    getindex()
    
    var image = document.getElementById('getImage');
    image.src = "out/y/img/" + index + ".png";
    var a = document.getElementById('interactive');
    a.href='out/y/interactive/'+index+'.html'
}

function previousClick(){
    timesClicked--;
    if(timesClicked < 0){
        timesClicked = 0;
    }
    setImage();
    return true 
}

function nextClick(){
    timesClicked++;
    setImage();
    return true 
}