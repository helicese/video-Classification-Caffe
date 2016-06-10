var data = {"raw": [["seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "backpack"], ["backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "seat belt", "microphone", "ping-pong ball", "mortar", "mortar", "ping-pong ball", "toilet seat", "mortar", "toilet seat", "barrel", "toilet seat", "vault", "toilet seat", "toilet seat", "barrel", "mortar"]], "num": 32, "struct": [0.23], "new": [["seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "seat belt", "seat belt"], ["backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "backpack", "ping-pong ball", "mortar", "mortar", "ping-pong ball", "mortar", "mortar", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat", "toilet seat"]]}
var rawData = data.raw;
var container = document.getElementById('visualization');
var legendContainer = document.getElementById('legend');
var circleContainer = document.getElementById('circle');
var rowContainer = document.getElementById('row');


console.log(data);

var COLORS = [
    '#FFC', '#CFF', '#FCC', '#9cc', '#FC9', 
    '#F99', '#969', '#c99', '#ff9', '#ccf',
    '#09c', '#ccc', '#f66', '#f96', '#9c6'];
var __catalog = [];
var __addCatalog = function(item) {
    if(__catalog.indexOf(item) == -1) {
        __catalog.push(item);
    }
}
var clearCatalog = function() {
    __catalog = [];
}

var _addBlock = function(item, tag, count) {
    __addCatalog(item);
    var block = document.createElement('span');
    block.className = tag;
    block.style.backgroundColor = COLORS[__catalog.indexOf(item)];
    block.title = item;
    (function(block, count){
        setTimeout(function(){
            block.style.opacity = 1;
        },100*count+2000);       
    })(block, count);

    rowContainer.appendChild(block);
}

var showBlock = function(input, tag) {
    var count = 0;
    var comment = document.createElement('span');
    comment.innerHTML = tag;
    comment.className = 'comment';
    rowContainer.appendChild(comment);
    for (var j = 0; j < input.length; j++) {
        if (input[j] instanceof Array) {
            for (var i = 0; i < input[j].length; i++) {
                _addBlock(input[j][i], tag, count);
                count ++;
            }            
        } else {
            _addBlock(input[j], tag, count);
            count ++;
        }
    }

    var lineBreaker = document.createElement('br');
    rowContainer.appendChild(lineBreaker);    
}
var showSeg = function(input) {
    for (var i = 0; i < input.length; i++) {
        var seg = document.createElement('div');
        seg.className = 'seg';      
        seg.style.left = data.num*20*input[i]+'px'; 
        // seg.style.top = 100px;
        (function(seg){
            setTimeout(function(){
                seg.style.opacity = 1;
                seg.style.top = '0px';
            },4000);             
        })(seg);
        rowContainer.appendChild(seg);

        var segComment = document.createElement('span');
        segComment.className = 'sComment';
        segComment.innerHTML = input[i]
        segComment.style.left = data.num*20*input[i]-10+'px';
        setTimeout(function(){
            segComment.style.opacity = 1;
        },4000)
        rowContainer.appendChild(segComment);        
    }
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
var _dataForCircle = function(input) {
    var circleData = new Int8Array(__catalog.length);
    for (var j = 0; j < input.length; j++) {
        if (input[j] instanceof Array) {
            for (var i = 0; i < input[j].length; i++) {
                circleData[__catalog.indexOf(input[j][i])]++;
            }            
        } else {
            circleData[__catalog.indexOf(input[j])]++;
        }
    }
    return circleData;
}

var showCircle = function(data) {
    var diameter = _dataForCircle(data.raw)
    console.log(diameter);
    for (var i = 0; i < diameter.length; i++) {
        var circleDom = document.createElement('div');
        circleDom.className = 'circle';
        circleDom.style.width = diameter[i]*15 +'px';
        circleDom.style.height = diameter[i]*15 + 'px';
        circleDom.style.backgroundColor = COLORS[i];
        circleDom.style.top = '0px';
        circleDom.style.left = '0px';
        (function(circleDom) {
            var circle = circleDom;
            setTimeout(function(){
                circle.style.top = Math.random()*100 + 'px';
                circle.style.left = Math.random()*550 + 'px';            
            },500);           
        })(circleDom);

        circleDom.title = __catalog[i];
        circleContainer.appendChild(circleDom);
    }
}
var fadeIn = function() {
    setTimeout(function(){
        legendContainer.style.opacity = 1;
        circleContainer.style.opacity = 1;
        rowContainer.style.opacity = 1;
    },0);  
}
var visualize = function (data) {
    if (typeof(data) == 'string') {
        data = JSON.parse(data);
    }
    clearCatalog();
    showBlock(data.raw, 'raw');
    showLegend(__catalog);
    showBlock(data.new, 'new');
    showCircle(data);
    showSeg(data.struct);   
    fadeIn();
}
// visualize(data);



