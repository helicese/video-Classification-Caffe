console.log('hello');
// var data = {"raw": [["seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "backpack"], ["backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "seat belt", "microphone", "ping-pong ball", "mortar", "mortar", "ping-pong ball", "toilet seat", "mortar", "toilet seat", "barrel", "toilet seat", "vault", "toilet seat", "toilet seat", "barrel", "mortar"]], "struct": [0.23], "new": [["seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "seat belt"], ["backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "ping-pong ball", "mortar", "mortar", "ping-pong ball", "mortar", "mortar", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat"]]}
var data = {"raw": [["seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "backpack"], ["backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "seat belt", "microphone", "ping-pong ball", "mortar", "mortar", "ping-pong ball", "toilet seat", "mortar", "toilet seat", "barrel", "toilet seat", "vault", "toilet seat", "toilet seat", "barrel", "mortar"]], "num": 32, "struct": [0.23], "new": [["seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "seat belt"], ["backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "ping-pong ball", "mortar", "mortar", "ping-pong ball", "mortar", "mortar", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat"]]}
// console.log(data)
var rawData = data.raw;
var container = document.getElementById('visualization');
var legendContainer = document.getElementById('legend');
var rowContainer = document.getElementById('row');

console.log(data);

var COLORS = ['#FFC', '#CFF', '#FCC', '#9cc', '#FC9', '#F99', '#969', '#c99', '#ff9', '#ccf'];
var colorBase = [];
var getColor = function(item) {
    if(colorBase.indexOf(item) == -1) {
        colorBase.push(item);
        return COLORS[colorBase.indexOf(item)];
    } else {
        return COLORS[colorBase.indexOf(item)];
    }
}

var addBlock = function(item, tag) {
    var block = document.createElement('span');
    block.className = tag;
    block.style.backgroundColor = getColor(item);
    block.title = item;
    rowContainer.appendChild(block);
}

var showLegend = function(input) {
    for (var i = 0; i < input.length; i++) {
        var wrapper = document.createElement('p');
        var color = document.createElement('span');
        var text = document.createElement('span');
        color.className = 'color';
        text.className = 'text'
        text.innerHTML = input[i];
        color.style.backgroundColor = COLORS[i];
        wrapper.appendChild(color);
        wrapper.appendChild(text);
        legendContainer.appendChild(wrapper);
    }
}

var showBlock = function(input, tag) {
    var comment = document.createElement('span');
    comment.innerHTML = tag;
    comment.className = 'comment';
    rowContainer.appendChild(comment);
    for (var j = 0; j < input.length; j++) {
        if (input[j] instanceof Array) {
            for (var i = 0; i < input[j].length; i++) {
                addBlock(input[j][i], tag);
            }            
        } else {
            addBlock(input[j], tag);
        }

    }

    var lineBreaker = document.createElement('br');
    rowContainer.appendChild(lineBreaker);    
}
var showStruct = function(input) {
    for (var i = 0; i < input.length; i++) {
        var seg = document.createElement('div');
        seg.className = 'seg';      
        seg.style.left = data.num*20*input[i]+'px';     
        rowContainer.appendChild(seg);

        var segComment = document.createElement('span');
        segComment.className = 'sComment';
        segComment.innerHTML = input[i]
        segComment.style.left = data.num*20*input[i]-10+'px';
        rowContainer.appendChild(segComment);        
    }


}

showBlock(data.raw, 'raw');
showLegend(colorBase);
showBlock(data.new, 'new');
showStruct(data.struct);


