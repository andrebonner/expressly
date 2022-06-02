<template>
  <a-carousel autoplay>
    <div>
      <img
        src="https://images.unsplash.com/photo-1515162305285-0293e4767cc2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1471&q=80"
      />
      <h1>Book church attendance Today</h1>
    </div>
    <div>
      <img
        src="https://images.unsplash.com/photo-1478147427282-58a87a120781?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80"
      />
      <h1>Book church attendance Today</h1>
    </div>
    <div>
      <img
        src="https://images.unsplash.com/photo-1497215728101-856f4ea42174?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80"
      />
      <h1>Book your space in line</h1>
    </div>
    <div>
      <img
        src="https://images.unsplash.com/photo-1497366216548-37526070297c?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1469&q=80"
      />
      <h1>Book your space in line</h1>
    </div>
  </a-carousel>
</template>
<style>
.ant-carousel {
  width: 100%;
}
.ant-carousel img {
  width: 100%;
  height: auto;
  vertical-align: middle;
}
.ant-carousel > .slick-active,
.slick-current h1 {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-size: 2rem;
  font-weight: bold;
  text-shadow: 0 0 10px #000;
  z-index: 999;
}
</style>
