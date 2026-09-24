const mongoose = require("mongoose");

mongoose
  .connect("mongodb://127.0.0.1:27017/deepshiva")
  .then(async () => {
    console.log("Mongo connected");

    const Test = mongoose.model(
      "Test",
      new mongoose.Schema({ name: String })
    );

    await Test.create({ name: "test-ok" });
    console.log("Write successful");
    process.exit(0);
  })
  .catch((err) => {
    console.error("Mongo write failed:", err.message);
    process.exit(1);
  });
