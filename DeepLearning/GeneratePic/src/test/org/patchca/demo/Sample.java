package test.org.patchca.demo;

import org.patchca.color.SingleColorFactory;
import org.patchca.filter.predefined.*;
import org.patchca.service.ConfigurableCaptchaService;
import org.patchca.utils.encoder.EncoderHelper;

import java.awt.Color;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

import javax.imageio.ImageIO;

/**
 * sample code
 * Created by shijinkui on 15/3/15.
 * 
 * org.patchca.word.RandomWordFactory里面设置字符串长度   AdaptiveRandomWordFactory设置内容
 */
public class Sample {
    public static void main(String[] args) throws IOException {

        ConfigurableCaptchaService cs = new ConfigurableCaptchaService();

        cs.setColorFactory(new SingleColorFactory(new Color(25, 60, 170)));
        cs.setFilterFactory(new CurvesRippleFilterFactory(cs.getColorFactory()));

        
        
//        String createdStr = EncoderHelper.getChallangeAndWriteImage(cs, "png", fos);
//        System.out.println(createdStr);
//        System.out.println("Done.");
//        fos.close();
        
        
        
        String createdStr = EncoderHelper.getChallangeImage(cs);
        System.out.println(createdStr);
        String savename = createdStr.trim() + ".png";
        FileOutputStream fos = new FileOutputStream(savename);
        EncoderHelper.WriteImage("png", fos);
        System.out.println("Done.");
        fos.close();
        

		final BufferedImage img = ImageIO.read(new File(savename));
		final int width = img.getWidth();
		final int height = img.getHeight();
		System.out.println(width + ":" + height);
    }
}
