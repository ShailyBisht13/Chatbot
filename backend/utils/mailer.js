const nodemailer = require("nodemailer");

const transporter = nodemailer.createTransport({
  service: "gmail",
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS, // Gmail App Password
  },
});

exports.sendOtp = async (email, otp) => {
  await transporter.sendMail({
    from: "DeepShiva <no-reply@deepshiva.ai>",
    to: email,
    subject: "DeepShiva OTP Verification",
    html: `
      <h2>Your OTP: ${otp}</h2>
      <p>Valid for 5 minutes.</p>
    `,
  });
};
