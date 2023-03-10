<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/llacroix/wsapp">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">WSApp</h3>

  <p align="center">
    Scalable WebSocket Application
    <br />
    <a href="https://github.com/llacroix/wsapp"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/llacroix/wsapp/tree/main/examples">View Demo</a>
    ·
    <a href="https://github.com/llacroix/wsapp/issues">Report Bug</a>
    ·
    <a href="https://github.com/llacroix/wsapp/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <!--
    <li><a href="#acknowledgments">Acknowledgments</a></li>
    -->
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--
[![Product Name Screen Shot][product-screenshot]](https://example.com)
-->

WSApp is a library that may helps making scalable websocket application by abstracting
the websocket out of your application. It is highly inspired by AWS GatewayAPI for WebSocket
application.

What this projects attempt to solve is to remove the websocket states from your application.
A simple implementation of websockets binds the websocket server to the http endpoint. In other
words, the application server becomes a manager of connection, websocket message dispatching etc.

The downside of this architecture is that it's not scalable. Since the software expect to receive
all connections on a single process. It means that if you had multiple websocket servers, the
connections on one instance wouldn't be able to communicate with the connections of an other
instance.

This library helps you design a websocket service that can be scaled and can dispatch request in
a multi process environment. The API of the connection manager would abstract the complexity
behind inter instance communication.

Currently, it's only possible to run it in a single process environment. But implementation with
a multi process environment is planned as it's the whole point of this project. It's just that
the simple implementation is simpler to implement obviously. What's important is that while
this library will handle certain use cases. It is developped in mind that it would be integrated
in an application instead of having an application integrated into wsapp. 
It is expected that the interfaces can be implemented to suit your needs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![AioHTTP][AioHttp]][AioHttp-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/llacroix/wsapp.git
   ```
2. Install it with pip
   ```
   cd wsapp/
   pip install -e .
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Check the examples/ folder for examples.

<!--
_For more examples, please refer to the [Documentation](https://wsapp.readthedocs.io/en/latest/)_
-->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add simple local managers and aiohttp integration
- [x] Added examples of a clustered websocket integration with 1 connections service 
- [x] Add handler manager with http backend
- [ ] Make scalable integration
	- [ ] Add a connection manager service with customizable backend
	- [x] Add integration with the remote connection manager service

See the [open issues](https://github.com/llacroix/wsapp/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## Contact

Loïc Faure-Lacroix - [@llacroix](https://twitter.com/llacroix) - lamerstar@gmail.com

Project Link: [https://github.com/llacroix/wsapp](https://github.com/llacroix/wsapp)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/llacroix/wsapp.svg?style=for-the-badge
[contributors-url]: https://github.com/llacroix/wsapp/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/llacroix/wsapp.svg?style=for-the-badge
[forks-url]: https://github.com/llacroix/wsapp/network/members
[stars-shield]: https://img.shields.io/github/stars/llacroix/wsapp.svg?style=for-the-badge
[stars-url]: https://github.com/llacroix/wsapp/stargazers
[issues-shield]: https://img.shields.io/github/issues/llacroix/wsapp.svg?style=for-the-badge
[issues-url]: https://github.com/llacroix/wsapp/issues
[AioHttp]: https://img.shields.io/badge/aiohttp-35495E?style=for-the-badge&logo=aiohttp&logoColor=4FC08D
[AioHttp-url]: https://docs.aiohttp.org/en/stable/
