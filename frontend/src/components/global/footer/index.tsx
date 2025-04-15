import React from "react";
import Lottie from "lottie-react";
import HeartAnimation from './heart.json'
import Heart2Animation from './heart2.json'


const Footer = () => {
    return (
        <div className="flex flex-col items-center justify-center w-full h-20 relative">
            <p className="font-medium text-foreground/70 flex items-center -space-x-4">Made with <Lottie animationData={HeartAnimation} loop={true} className="w-14 p-0 m-0" /> by Devs Rec</p>
            {/* <Lottie animationData={Heart2Animation} loop={true} className="absolute w-14 -top-20t-1/2 -translate-x-1/2"/>  */}
        </div>
    )
}

export default Footer