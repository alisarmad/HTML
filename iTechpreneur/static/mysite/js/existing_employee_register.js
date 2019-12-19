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


// function validUrl(sUrl)
// {

//   url = 'www.google.com'
//   url_validate = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
//   var url =('https://'+ sUrl)
//   url_validate.test(url)
//   if(url_validate.test(url))
//   {
//      return true;
//   }
//   else
//     {
//        return false;
//     }
// }

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

$(document).on('click','#employee_sign_up_btn',function(e){
 console.log("Hello !!")  
var first_name = $('#first_name').val();
var surname = $('#surname').val();
var email = $('#email').val();
var password = $('#password').val();
var date_of_birth = $('#date_of_birth').val();
var position_in_company = $('#position_in_company').val();
var website_url = $('#website_url').val();
var address = $('#address').val();
var country =$('#country option:selected').val();
var phone_number = $('#phone_number').val();
var company_registration_number = $('#company_registration_number').val();
var skills_interested = $('#skills_interested option:selected').val();
var industry_interested = $('#industry_interested option:selected').val();
var token=$('input[name="csrfmiddlewaretoken"]').val();

  first_name = first_name.trim()
  surname = surname.trim()
  date_of_birth = date_of_birth.trim()
  email = email.trim()
  address = address.trim()
  website_url = website_url.trim()


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






if(date_of_birth =='')
{
   $("#date_of_birth_error").text('Please enter DOB correctly.');
    document.getElementById("date_of_birth_error").style.color = "red";
    return false;
}
else
{
 $("#date_of_birth_error").text('');
    document.getElementById("date_of_birth_error").style.color = "red"; 
}





 if(position_in_company.length == 0)
 {
  $("#position_in_company_error").text('Enter the Position in Company.');
      document.getElementById("position_in_company_error").style.color = "red";
      return false;
 }

 if(position_in_company.length > 25)
  {

    $("#position_in_company_error").text('Max length is 25.');
        document.getElementById("position_in_company_error").style.color = "red";

    return false;

  }
  if(position_in_company.length > 0 && position_in_company.length <= 25)
  {
    $("#position_in_company_error").text('')
    console.log('position_in_company done.')
  }





  if(website_url.length == 0)
  {
    $("#website_url_error").text('website url is required.');
    document.getElementById("website_url_error").style.color = "red";
    return false;
  }

  if(website_url.length > 25)
  {

    $("#website_url_error").text('Max length of website_url is 25.');
        document.getElementById("website_url_error").style.color = "red";

    return false;

  }
  if(website_url.length > 0 && website_url.length <= 25)
  {
    $("#website_url_error").text('')
    console.log('website_url_error done.')
  }





if(address.length == 0)
 {
  $("#address_error").text('Enter the address.');
      document.getElementById("address_error").style.color = "red";
      return false;
 }

 if(address.length > 25)
  {

    $("#address_error").text('Max length of Address is 25.');
        document.getElementById("address_error").style.color = "red";

    return false;

  }
  if(address.length > 0 && address.length <= 25)
  {
    $("#address_error").text('')
    console.log('address done.')
  }



if(country.length ==0)
{
  
  $("#country_error").text('Select  the Skills Interested.');
        document.getElementById("country_error").style.color = "red";

    return false;
}
if(country.length !=0 )
{
$("#country_error").text('');
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






 if(company_registration_number.length == 0)
 {
  $("#company_registration_number_error").text('Enter the Company Registration Number.');
      document.getElementById("company_registration_number_error").style.color = "red";
      return false;
 }

 if(company_registration_number.length > 25)
  {

    $("#company_registration_number_error").text('Max length of Company Registration Number is 25.');
        document.getElementById("company_registration_number_error").style.color = "red";

    return false;

  }
  if(company_registration_number.length > 0 && company_registration_number.length <= 25)
  {
    $("#company_registration_number_error").text('')
    console.log('address done.')
  }








if(skills_interested.length ==0)
{
  
  $("#skills_interested_error").text('Select  the Skills Interested.');
        document.getElementById("skills_interested_error").style.color = "red";

    return false;
}
if(skills_interested.length !=0 )
{
 $("#skills_interested_error").text('');
}






if(industry_interested.length ==0)
{
  
  $("#industry_interested_error").text('Select  the Skills Interested.');
        document.getElementById("industry_interested_error").style.color = "red";

    return false;
}
if(industry_interested.length !=0 )
{
 $("#industry_interested_error").text('');
}




console.log("before ajax")
  $.ajax({
    url: '/existing_employee_registration/',
    type: "POST",
    data: {'first_name':first_name,'surname':surname,'email':email,'password':password,'date_of_birth':date_of_birth,'position_in_company':position_in_company,'website_url':website_url,'address':address,'country':country,'phone_number':phone_number,'company_registration_number':company_registration_number,'skills_interested':skills_interested,'industry_interested':industry_interested,'csrfmiddlewaretoken':token },
    dataType: 'json',
    cache: false,


    success: function(response){        
     if(response=='1')
      {
        console.log(response)
        alert("Registration done.");
        // $('#info_model').modal('show');
        // $("#p_text").text("Registration done.");
        window.location.href='/login/';
      }
      else
      {
        if(response=='0')
        {
          // alert('Username already registered.');
          console.log(response)
          console.log('done.')
          alert('E-mail already registered.');
          // document.getElementById("email_txt").style.color = "red";
          return false;
        }       
      }
    }
  });
});























