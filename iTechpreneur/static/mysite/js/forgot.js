function validateEmail(sEmail) 
{
  var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
  if (filter.test(sEmail)) 
  {
      return true;
  }
  else 
  {
      return false;
  }
}

// $(document).ready(function () {
//    $('input[type=text]').on('keypress', function(e) {
//       if (e.which == 32)
//       {
//         console.log('no space')
//         return false;
//       }
//   });
// });

$(document).ready(function () {
$('#email').keypress(function( e ) {
       if(e.which === 32) 
         return false;
    });
});

$(document).on('click','#forgot_btn',function(e){  
  var username= $('#username').val();
  var token=$('input[name="csrfmiddlewaretoken"]').val()
  username = username.trim()


 if(username.length == 0)
  {
    $("#email_error").text('Email is required.');
    document.getElementById("email_error").style.color = "red";
    return false;
  }
  else
  {
    if(validateEmail(username))
    {
      console.log('valid email');
      $("#email_error").text('');
    }
    else
    {
      $("#email_error").text('Enter valid email.');
      document.getElementById("email_error").style.color = "red";
      return false;
    }
  }

console.log('before ajax');
     // $('.loader').show();

  $.ajax({
    url: '/forgot/',
    type: "POST",
    data: {'username':username,'csrfmiddlewaretoken':token},
    dataType: 'json',
    cache: false,
    success: function(response){
      // $('.loader').hide();
      console.log(response)
     if(response=='1')
      { 
        
        // $('#forgot_info_model').modal('show');
        // $("#forgot_p_text").text("New Password has been sent to your registered email.");
        alert("New Password has been sent to your registered Email.");
        window.location.href='/login/';
      }
      else
      {
        if(response=='0')
          { 

            // $("#username_txt").text('Enter registered Email.');
            // document.getElementById("username_txt").style.color = "red";
            alert('Enter registered Email.');
          }
        if(response=='2')
        {
          // $('#info_model').modal('show');
          // $("#p_text").text("Unable to connect server.");
          alert('Unable to connect server.');
        }
        
      }
    }
  });
});

// $(document).on('click','#forgot_close_reload_symbol',function(e){  
//   window.location.href='/login/';
//   });

// $(document).on('click','#forgot_close_reload',function(e){  
//   window.location.href='/login/';
//   });