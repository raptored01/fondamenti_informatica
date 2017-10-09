/*global $, jQuery, alert*/

human_picked_matches = 0;
world_matches = 15;

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function human_pick(match) {
  "use strict";
  if (human_picked_matches < 3) {
    human_picked_matches += 1;
    world_matches -= 1;
    $(match).remove();
  } else {
    alert("You can pick a maximum of three matches!")
  }
}

function bot_pick() {
  "use strict";

  /*
  AI Logic:
  The winning strategy consists in picking a number of matches so that the
  other player would be left with a number such that number - 1 is divisible
  by 4.
  */

  var pick;
  var ok = false;

  /*
  Since there will be a condition where the AI will pick a random number of matches
  a while loop is due in order to check if that is a valid number (see las if's).
  The variable ok is used as a flag to escape the loop if the picked number is valid
  */

  while (!ok) {
    if ((world_matches - 1) % 4 == 0) {
      /*
      If the human player gets the AI to a likely loosing condition, the AI
      will pick a random number of matches, hoping for a player mistake
      */
      pick = getRandomInt(1, 3);
    } else if (world_matches <= 4) {
      /*
      If the number of matches left on the table is less than or equal to 4,
      to win it's sufficient to pick a number of matches so that left-picked = 1
      */
      pick = world_matches - 1;
    } else {
      /*
      If none of the above condition are met, the AI will have to chose the right number
      of matches to comply with the winning strategy.
      To do so it iterates in a for loop all the values from 1 to 3 and checks whether
      (the value - the number of matches) is divisible by 4. If so, it will pick said
      number of mathces.
      */
      for (var n = 1; n < 4; n++) {
        if ((world_matches - n - 1) % 4 == 0) {
          pick = n;
          break
        }
      }
    }

    if (pick < world_matches) {
      /*
      This condition verifies if the number picked by the algorithm is valid.
      It is necessary because when it is chosen randomly, it might be necessary to
      pick it again.
      Being the number a valid move, it will iterate through the DOM ".match" elements
      and remove an according number of them. Done that, it will set the escape flag
      ok to true, breaking out the while loop.
      */
      world_matches -= pick;
      var n = 0;
      $(".match").each(function () {
        if (n < pick) {
          $(this).remove();
          n += 1;
        }
      })
      ok = true;
    }
  }
  $("#nMatches").val(world_matches);
}

function check_victory(player) {
  if (world_matches == 1) {
    setTimeout(function () {
        alert(player + " wins!");
        $("#start_player").val(1);
        reset(15);
        }, 1000);
    return true;
  } else {
    return false;
  }
}

function reset(matches) {
  "use strict";
  $(".match").remove();
  world_matches = matches;
  human_picked_matches = 0;
  for (var i=0; i <world_matches; i++) {
    var match = document.createElement("img");
    match.src = static_img
    $(match).attr("num", i)
    $(match).attr("class", "match")

    $(match).css({
        "width": "50px",
        "height": "150px"
    });
    $("#game-table").append(match)
  }
  $("#nMatches").val(world_matches);
  $(".match").bind("click", function() {
    human_pick($(this))
    $("#nMatches").val(world_matches)
  })
  if ($("#start_player").val() == 2) {
    bot_pick();
  }
}

$(document).ready(function () {

  reset(15);
  $("#nMatches").val(world_matches)


  $("#ok").bind("click", function () {
    if (human_picked_matches > 0) {
      human_picked_matches = 0
      if (!(check_victory("Human player"))) {
        bot_pick();
        check_victory("Stupid AI");
      }
    } else {
      alert("You must pick at least a match!");
    }
  });

  $("#reset").bind("click", function () {
      $("#start_player").val(1);
      reset(15);
    });

  $("#btn-minus").bind("click", function () {
    $("#start_player").val(1);
    if (world_matches > 5) {
      reset(world_matches-1);
    }
  });

  $("#btn-plus").bind("click", function () {
    $("#start_player").val(1);
    if (world_matches < 100) {
      reset(world_matches+1);
    }
  });

  $("#nMatches").bind("input", function () {
    var val = $(this).val();
    if (val >= 5 && val <=100) {
      reset(val);
    }
  });

  $("#start_player").bind("input", function () {
    reset(world_matches)
  })

})
