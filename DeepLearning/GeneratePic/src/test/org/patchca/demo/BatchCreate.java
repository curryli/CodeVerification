package test.org.patchca.demo;

import java.awt.Color;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Random;

import org.patchca.color.SingleColorFactory;
import org.patchca.filter.predefined.CurvesRippleFilterFactory;
import org.patchca.service.ConfigurableCaptchaService;
import org.patchca.utils.encoder.EncoderHelper;

public class BatchCreate {
	public static int N=1000;
	
	public static String getRandomString(int length) { //length表示生成字符串的长度  
	    String base = "abcdefghijklmnopqrstuvwxyz0123456789";     
	    Random random = new Random();     
	    StringBuffer sb = new StringBuffer();     
	    for (int i = 0; i < length; i++) {     
	        int number = random.nextInt(base.length());     
	        sb.append(base.charAt(number));     
	    }     
	    return sb.toString();     
	 }    
	
	public static void main(String[] args) throws IOException {
		for(int i=0;i<N;i++){
			//System.out.println(i);
			ConfigurableCaptchaService cs = new ConfigurableCaptchaService();

	        cs.setColorFactory(new SingleColorFactory(new Color(25, 60, 170)));
	        cs.setFilterFactory(new CurvesRippleFilterFactory(cs.getColorFactory()));
	        
	        String createdStr = EncoderHelper.getChallangeImage(cs);
	        //System.out.println(createdStr);
	        String savename = "createdImg/" + createdStr.trim() + "_" + getRandomString(4) + ".png";
	        File file =new File(savename);
	        if(!file.exists())
	          {       
	            file.createNewFile();
	            FileOutputStream fos = new FileOutputStream(file,true);
	            EncoderHelper.WriteImage("png", fos);
		        fos.close();
	          }
	    }
		
		System.out.println("All Done.");
		
		
		
	}

}
