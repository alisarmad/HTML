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

// $(document).on('click','#close_reload',function(e){  
//       location.reload(true);
// });


// $(document).on('click','#close_reload_symbol',function(e){  
//       location.reload(true);
// });

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
$('#password').keypress(function( e ) {
       if(e.which === 32) 
         return false;
    });
$('#first_name').keypress(function( e ) {
       if(e.which === 32) 
         return false;
    });
$('#surname').keypress(function( e ) {
       if(e.which === 32) 
         return false;
    });
$('#email').keypress(function( e ) {
       if(e.which === 32) 
         return false;
    });




$(document).on('click','#student_sign_up_btn',function(e){
 
  var first_name = $('#first_name').val();
  var surname = $('#surname').val();
  var email = $('#email').val();
  var password =$('#password').val();
  var technical_subject = $('#technical_subject option:selected').val();
  var student_type= $('#student_type option:selected').val();
  var country =$('#country option:selected').val();
  var token=$('input[name="csrfmiddlewaretoken"]').val()
  first_name = first_name.trim();
  surname = surname.trim();
  email = email.trim();
  password = password.trim();
  technical_subject = technical_subject.trim();
  student_type = student_type.trim();
  country = country.trim();

if(first_name.length != 0 && surname.length != 0 && email.length != 0 && password.length != 0 && technical_subject.length != 0 && student_type.length !=0 && country.length != 0 ){
    
   
    $(this).addClass("active");
    $(this).removeClass("btn-yellow");
    $('.processing').css("display","block");
}


  


 if(first_name.length == 0)
 {
    // alert('First_name is required');
    $("#first_name_error").text('First Name is required.');
    document.getElementById("first_name_error").style.color = "red";
    return false;
 }
 else
 {
   if (first_name.match(/^[a-zA-Z\s]+$/))
     {
       first_name = first_name.replace(/  +/g, ' '); 
      
       $("#first_name_error").text('');
       // alert('valid');  
     }
   else
     {
       // alert('invalid')
       // alert('Only alphabets are allowed for this field.');
      $("#first_name_error").text('Only alphabets are allowed for this field.');
      document.getElementById("first_name_error").style.color = "red";
      return false;
     }

   
 }

  if(first_name.length > 25)
  {
    $("#first_name_error").text('Max length of Name is 25.');
    document.getElementById("first_name_error").style.color = "red";
    return false;
  }
  if(first_name.length > 0 && first_name.length <= 25)
  {
    console.log('name done.')
    $("#first_name_error").text('');
  }




if(surname.length == 0)
 {
    // alert('First_name is required');
    $("#surname_error").text('Last Name is required.');
    document.getElementById("surname_error").style.color = "red";
    return false;
 }
 else
 {
   if (surname.match(/^[a-zA-Z\s]+$/))
     {
       surname = surname.replace(/  +/g, ' '); 
      
       $("#surname_error").text('');
       // alert('valid');  
     }
   else
     {
       // alert('invalid')
       // alert('Only alphabets are allowed for this field.');
      $("#surname_error").text('Only alphabets are allowed for this field.');
      document.getElementById("surname_error").style.color = "red";
      return false;
     }

   
 }

  if(surname.length > 25)
  {
    $("#surname_error").text('Max length of Last Name is 25.');
    document.getElementById("first_name_error").style.color = "red";
    return false;
  }
  if(surname.length > 0 && surname.length <= 25)
  {
    
    $("#surname_error").text('');
  }









 if(email.length == 0)
  {
    $("#email_error").text('Email is required.');
    document.getElementById("email_error").style.color = "red";
    return false;
  }
  else
  {
    if(validateEmail(email))
    {
      
      $("#email_error").text('');
    }
    else
    {
      $("#email_error").text('Enter valid email.');
      document.getElementById("email_error").style.color = "red";
      return false;
    }
  }


if(technical_subject.length == 0){
  $("#technical_subject_error").text('Select Your Technical Subject');
        document.getElementById("technical_subject_error").style.color = "red";
        return false;
}
if(technical_subject.length !=0){
  $("#technical_subject_error").text('');
}

if(student_type.length == 0){
  $("#student_type_error").text('Select Your Technical Subject');
        document.getElementById("student_type_error").style.color = "red";
        return false;
}
if(technical_subject.length !=0){
  $("#student_type_error").text('');
}

if(country.length ==0)
{
  
  $("#country_error").text('Select  Your Country.');
        document.getElementById("country_error").style.color = "red";

    return false;
}

if(country.length !=0 )
{
$("#country_error").text('');
}




  if(password.length == 0)
  {
    $("#password_error").text('Password is required.');
      document.getElementById("password_error").style.color = "red";
    return false; 
  }

  if(password.length > 8)
  {
    
   }
   else
  {
    $("#password_error").text('Min length of password is 8.');
        document.getElementById("password_error").style.color = "red";

    return false;    
  }

 
  $.ajax({
    url: '/student_registration/',
    type: "POST",
    data: {'first_name':first_name,'surname':surname,'email':email,'password':password,'country':country,'technical_subject':technical_subject,'student_type':student_type,'csrfmiddlewaretoken':token },
    dataType: 'json',
    cache: false,
    success: function(response){
     // if(response == '3')
     //  {
     //    // alert('Email already registered.');
     //    $("#email_txt").text('Email already registered.');
     //    document.getElementById("email_txt").style.color = "red";
     //    return false;
     //  }
     
        
     if(response=='1')
      {

        
        $('#student_sign_up_btn').removeClass("active");
        $('#student_sign_up_btn').addClass("btn-yellow");
        $('.processing').css("display", "none");
        $('.success').css('display','block');
       
        return false;
      }
      else
      {
        if(response=='0')
        {
          $('#student_sign_up_btn').removeClass("active");
          $('#student_sign_up_btn').addClass("btn-yellow");
          $('.processing').css("display", "none");
          $('.failure').css('display','block');
          return false;
        }       
      }
    }
  });
});


  

$(document).ready(function () {



  $('#confirm_password').keypress(function (e) {
    if (e.keyCode == 13)
    {
      $('#confirm_password').click();
    }
  });
});


});
