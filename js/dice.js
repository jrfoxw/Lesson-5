/*
    Sword Shield Book  - Rock Paper Scissors style game.
    Rules:
    Play: Player clicks Roll button

    Each 'Die' changes to a random image,
    Sword, Book, Shield
    Sword beats Magic
    Magic beats Shield
    Shield beats Sword.

    Two like items, cancel each other out.
*/


// Declare Globals for Player and Computer



var shieldNum = 5;
var bookNum = [10,6];

var highIndex = 3;
var randomRoll = 15;
var mustWin = 10;
var Pscore = [];
var Cscore = [];
var player = [];
var computer = [];
var winner = "";

$(function(){

    $('#b1').click(function(){

    var store = [];

         $.each(['#p1','#p2','#p3','#c1','#c2','#c3'], function(index, value){
         random_pull(value);

           })


        console.log('Player = ',Pscore);
        console.log('Computer = ',Cscore);
        compare_results(Pscore, Cscore);

        // Clear player, computer storage
        Pscore = [];
        Cscore = [];
    })

    $('#b0').click(function(){

        zeroed_score = 0
        $('#pscore').html(zeroed_score);
        $('#cscore').html(zeroed_score);
        $('#b1').show();
        $(location).attr('href','/dice.html');
    })
})



function random_pull(square){

        var number = Math.floor(Math.random() * randomRoll + 1);
        var hnumber = bookNum[0]
        var lnumber = bookNum[1]

        if (number <= shieldNum){
            $(square).css('background-image','url("/images/shield.png")');
            $(square).css('background-size','84px 84px');
            if (square == '#p1' || square == '#p2' || square == '#p3') {
            Pscore.push('shield');
            }else{
            Cscore.push('shield');
            }

        }else if (number <= hnumber && number >= lnumber){
            $(square).css('background-image','url("/images/magic.png")');
            $(square).css('background-size','64px 64px');
            if (square == '#p1' || square == '#p2' || square == '#p3'){
            Pscore.push('magic');
            }else{
            Cscore.push('magic');
            }
        }else{
            $(square).css('background-image','url("/images/sword3.png")');
            $(square).css('background-size','64px 64px');
            if (square == '#p1' || square == '#p2' || square == '#p3'){
            Pscore.push('sword');
            }else{
            Cscore.push('sword');
            }
        }


}


function compare_results(player1, player2){

        var play_resolutions = [['shield','sword'],['magic','shield'],
                                ['sword','magic']]
        var win_tabulate = 1

        console.log('Comparing Results...');
        for (i = 0; i < highIndex; i++){
        $.each([play_resolutions[i]],function(index, value){
            console.log('P-Value ', value[0]);

            if
                (player1[i] == value[0] && player2[i] == value[1]){
                    player.push(win_tabulate)
            }else if
                (player2[i] == value[0] && player1[i] == value[1]){
                    computer.push(win_tabulate)
            }

       });
    };

    console.log('PLAYER FINAL ', player);
    console.log('CPU FINAL ', computer);



    if (player.length == computer.length){
        console.log('NO WINNER ---> TIE ')

    }else if( player.length > computer.length ){
        console.log('|--------------------|');
        console.log('| PLAYER WINS ROUND! |');
        console.log('|--------------------|');
        addPoint('#pscore');
        winner = 'Player';

    }else{
        console.log('|----------------------|');
        console.log('| COMPUTER WINS ROUND! |');
        console.log('|----------------------|');
        addPoint('#cscore');
        winner = 'Computer';
    }


     player = [];
     computer = [];
     checkForWinner();
}


function addPoint(value){
    var score_add = 1;
    if (value == '#pscore'){
        var player_point = Number($(value).html());
            player_point += score_add;
            $(value).html(player_point);
            console.log('PLAYER SCORE ', player_point);
    }else{
        var cpu_point = Number($(value).html());
            cpu_point += score_add;
            $(value).html(cpu_point);
            console.log('CPU SCORE ', cpu_point);
    }

}



function checkForWinner(){

    if ($('#pscore').html() >= mustWin || $('#cscore').html() >= mustWin){
        console.log('Game over !!')
        $('#instructions').html('GAME OVER <br>'+winner+' Wins!!, <br> Press RESET.')
        $('#b1').hide()

    }


}





