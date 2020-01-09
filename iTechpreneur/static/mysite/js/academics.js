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
$('#date_of_birth').keypress(function( e ) {
         return false;
    });
});

// first_name
// surname
// title
// email
// university_name
// university_address
// phone_number
// programme_title
// position
// subject_area
// password

$(document).on('click','#student_sign_up_btn',function(e){
 console.log("Hello !!")  
  var first_name = $('#first_name').val();
  var surname = $('#surname').val();
  var title = $('#title option:selected').val();
  var email = $('#email').val();
  var university_name = $('#university_name').val();
  var university_address= $('#university_address').val();
  var phone_number =$('#phone_number').val();
  var programme_title =$('#programme_title').val();
  var position =$('#position option:selected').val();
  var subject_area =$('#subject_area option:selected').val();
  var password =$('#password').val();
  var token=$('input[name="csrfmiddlewaretoken"]').val()
  first_name = first_name.trim()
  surname = surname.trim()
  email = email.trim()
  if(first_name.length != 0 && surname.length != 0 && email.length != 0 && password.length != 0 && technical_subject.length != 0 && country.length != 0 ){
    alert("hello")
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
       console.log('name done.')
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
       console.log('name done.')
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
    console.log('name done.')
    $("#surname_error").text('');
  }




if(title.length ==0)
{
  
  $("#title_error").text('Select the title.');
        document.getElementById("title_error").style.color = "red";

    return false;
}
if(title.length !=0 )
{
$("#title_error").text('');
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


if(university_name.length == 0)
 {
  $("#university_name_error").text('Enter the University Name.');
      document.getElementById("university_name_error").style.color = "red";
      return false;
 }

 if(university_name.length > 25)
  {

    $("#university_name_error").text('Max length of University Name is 25.');
        document.getElementById("university_name_error").style.color = "red";

    return false;

  }
  if(university_name.length > 0 && university_name.length <= 25)
  {
    $("#university_name_error").text('')
    console.log('address done.')
  }




  if(university_address.length == 0)
 {
  $("#university_address_error").text('Enter the University Address.');
      document.getElementById("university_address_error").style.color = "red";
      return false;
 }

 if(university_address.length > 25)
  {

    $("#university_address_error").text('Max length of University Address is 25.');
        document.getElementById("university_address_error").style.color = "red";

    return false;

  }
  if(university_address.length > 0 && university_address.length <= 25)
  {
    $("#university_address_error").text('')
    console.log('address done.')
  }



  if(phone_number.length == 0)
 {
  $("#phone_number_error").text('Enter the Phone Number.');
      document.getElementById("phone_number_error").style.color = "red";
      return false;
 }

 if(phone_number.length > 15)
  {

    $("#phone_number_error").text('Max length of Phone Number is 15.');
        document.getElementById("phone_number_error").style.color = "red";

    return false;

  }
  if(phone_number.length > 0 && phone_number.length <= 15)
  {
    $("#phone_number_error").text('')
    console.log('address done.')
  }




  if(phone_number.length == 0)
 {
  $("#phone_number_error").text('Enter the Phone Number.');
      document.getElementById("phone_number_error").style.color = "red";
      return false;
 }

 if(phone_number.length > 15)
  {

    $("#phone_number_error").text('Max length of Phone Number is 15.');
        document.getElementById("phone_number_error").style.color = "red";

    return false;

  }
  if(phone_number.length > 0 && phone_number.length <= 15)
  {
    $("#phone_number_error").text('')
    console.log('address done.')
  }



  if(position.length ==0)
{
  
  $("#position_error").text('Select the Position.');
        document.getElementById("position_error").style.color = "red";

    return false;
}
if(position.length !=0 )
{
$("#position_error").text('');
}



  if(subject_area.length ==0)
{
  
  $("#subject_area_error").text('Select the Subject Area.');
        document.getElementById("subject_area_error").style.color = "red";

    return false;
}
if(subject_area.length !=0 )
{
$("#subject_area_error").text('');
}


 if(password.length == 0)
  {
    $("#password_error").text('Password is required.');
      document.getElementById("password_error").style.color = "red";
    return false; 
  }

  if(password.length > 8)
  {
    console.log('pass done.')
   }
   else
  {
    $("#password_error").text('Min length of password is 8.');
        document.getElementById("password_error").style.color = "red";

    return false;    
  }


  console.log("before ajax")
  $.ajax({
    url: '/teacher_registration/',
    type: "POST",
    data: {'first_name':first_name,'surname':surname,'title':title,'email':email,'university_name':university_name,'university_address':university_address,'phone_number':phone_number,'programme_title':programme_title,'position':position,'subject_area':subject_area,'password':password,'csrfmiddlewaretoken':token },
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
        alert(response)
        console.log(response)
        $('#student_sign_up_btn').removeClass("active");
        $('#student_sign_up_btn').addClass("btn-yellow");
        $('.processing').css("display", "none");
        $('.success').css('display','block');
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



