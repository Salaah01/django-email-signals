const TerserPlugin = require("terser-webpack-plugin");

module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        },
      },
      {
        test: /\.(scss|css)$/,
        use: [
          "style-loader",
          {
            loader: "css-loader",
            options: {
              importLoaders: 1,
              modules: true,
            },
          },
          "sass-loader",
        ],
        include: /\.module\.(scss|css)$/,
      },
      {
        test: /\.(scss|css)$/,
        use: ["style-loader", "css-loader", "sass-loader"],
        exclude: /\.module\.(scss|css)$/,
      },
      {
        test: /\.svg$/,
        use: "file-loader",
      },
      {
        test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        use: [
          {
            loader: "file-loader",
            options: {
              name: "[name].[ext]",
              outputPath: "fonts/",
            },
          },
        ],
      },
      {
        test: /\.(ts|tsx)$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: [".ts", ".js", ".tsx"],
  },
  optimization: {
    minimizer: [new TerserPlugin()],
  },
};