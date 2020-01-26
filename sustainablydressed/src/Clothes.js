import React from 'react';
import Image from './Image';

const Clothes = () => {
    return(
        <div>
            <Image src={'https://cf-assets-thredup.thredup.com/assets/201819095/retina.jpg'} width={200} height={200} mode='fit'/>
            <h1>Title</h1>
            <p>Price</p>
        </div>
    )
}

export default Clothes