def html(code):
    mail_sub = f"""
                 <!DOCTYPE html>
                 <html lang="en-GB" style="background: rgba(212, 212, 212, 0.322);"> 
            <head> 
              <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
              <title>Tamu - Its easier this way</title>
              <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                 <style type="text/css">
                 </style>
             </head> 
             <body style="margin: 0; padding: 0; background: rgba(212, 212, 212, 0.322);" >
             <table role="presentation" border="0"  align="center" cellpadding="0" cellspacing="0" width="100%">
                 <tr> 
                    <td style="padding: 10px 0 30px 0;">
                         <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse; border:0 ;"> 
                            <tr>
                                <td align="center" style="padding: 0px 0 6px 0;">
                                    <img  src="https://exodus-bucket.s3.amazonaws.com/exodus_logo.png" alt="Exodus Logo" width="100" height="auto" style="display: block; padding: 2px;" /> 

                                  </td>
                                  <tr> 
                                    <td bgcolor="#ffffff" style="padding: 10px 30px 50px 30px;"> 
                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;"> 
                                            <tr>
                                                <td style="color: #020202; font-family: Inter, sans-serif;"> 
                                                  <p align="center" style=" font-size: 16px; ">Welcome to Exodus 🎉 </p> 
                                                    <h1 align="center" style="font-size: 18px; font-weight:normal; margin:10px; color: #000000;">Your verification code is</h1>
                                                  </td> 
                                            </tr>
                                            <tr>
                                                <td style="color: #00000; font-family: Inter, sans-serif; line-height: 24px; padding: 20px 0 30px 0;">
                                                 <p align="center" style="color: #000000;background-color: #ffffff; font-size: 40px; font-weight: bold; letter-spacing:2px; margin: 0;">
                                                 {str(code)}</p> 
                                                </td> 
                                              </tr> 
                                        </table> 
                                    </td> 
                                  </tr> 
                            </tr> 
                            <tr> 
                                <td align="center"  style="padding: 0px 30px;"> 
                                    <table  border="0" cellpadding="0" cellspacing="0"  width="100%" style="border-collapse: collapse;"> 
                                    <tr align="center"> 
                                      <td style="color: grey; padding:20px;" align="center"> 
                                        <p  style="margin-left: 0; font-family: Inter, sans-serif; font-size: 10px;">Please do not reply to this email 
                                       <!-- <a href="#" style="color: grey;">Unsubscribe</a></p> -->                                
                                       <p  style="font-family: Inter, sans-serif; font-size: 10px;">Copyright 2023. Tamu</p> 
                                      </td> 
                                    </tr>
                                  </table> 
                                </td>
                              </tr> 
                         </table> 
                        </td> 
                    </tr> 
                </table> 
            </body> 
            </html>
    """

    return mail_sub