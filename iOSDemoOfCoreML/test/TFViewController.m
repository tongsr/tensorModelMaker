//
//  TFViewController.m
//  test
//


#import "TFViewController.h"
#import <CoreML/CoreML.h>
#import "HWModel.h"



//coreml教程
//https://www.jianshu.com/p/174b7b67acc9

@interface TFViewController ()
- (IBAction)readImageFunc:(id)sender;

@end

@implementation TFViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    HWModel *hwmodel=[[HWModel alloc]init];
    MLMultiArray *mlarray=[[MLMultiArray alloc]initWithShape:@[@1,@32,@32] dataType: MLMultiArrayDataTypeFloat32 error:nil];
    NSString *path = [[NSBundle mainBundle] pathForResource:@"6_66" ofType:@"txt"];
    NSString* content = [NSString stringWithContentsOfFile:path encoding:NSUTF8StringEncoding error:nil];
    content = [content stringByReplacingOccurrencesOfString:@"\r" withString:@""];
    NSArray *strArr = [content componentsSeparatedByString:@"\n"];
    
    for (int i =0; i<32; i++) {
        NSString *str = [strArr objectAtIndex:i];
        for (int j=0; j<32; j++) {
            NSString *charactor=[str substringWithRange:NSMakeRange(j, 1)];
            NSNumber *num = [NSNumber numberWithInt:[charactor intValue]];
            NSNumber *numi=[NSNumber numberWithInt:i];
            NSNumber *numj=[NSNumber numberWithInt:j];
            [mlarray setObject:num forKeyedSubscript:@[@0,numi,numj]];
        }
    }
    
    HWModelInput *input=[[HWModelInput alloc]initWithEval_input__0:mlarray];
    HWModelOutput *output=[hwmodel predictionFromFeatures:input error:nil];
    NSLog(@"%@",[output.op_to_store__0 objectForKeyedSubscript:@[@0,@0,@0]]);
    
    
    UIImage *image = [UIImage imageNamed:@"6.jpg"];
    [self imageToArray:image];

}




-(NSArray *)imageToArray:(UIImage *)image{
    image = [self getGrayImage:image];
    image = [self scaleToSize:image size:CGSizeMake(32, 32)];
    
    //将图片转为data数据
    NSData *imageData = UIImageJPEGRepresentation(image, 1.0);
    NSUInteger len = [imageData length];
    Byte *byteData = (Byte*)malloc(len);
    id a = (__bridge id)(memcpy(byteData, [imageData bytes], len));
    
    CGImageRef cgimg = [image CGImage];
    CFDataRef data = CGDataProviderCopyData(CGImageGetDataProvider(cgimg));
    const unsigned char * buffer =  CFDataGetBytePtr(data);
    NSLog(@"%s",buffer);
    NSArray *array;
    return array;
}


-(UIImage*)getGrayImage:(UIImage*)sourceImage
{
    int width = sourceImage.size.width;
    int height = sourceImage.size.height;
    
    CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceGray();
    CGContextRef context = CGBitmapContextCreate (nil,width,height,8,0,colorSpace,kCGImageAlphaNone);
    CGColorSpaceRelease(colorSpace);
    
    if (context == NULL) {
        return nil;
    }
    
    CGContextDrawImage(context,CGRectMake(0, 0, width, height), sourceImage.CGImage);
    UIImage *grayImage = [UIImage imageWithCGImage:CGBitmapContextCreateImage(context)];
    CGContextRelease(context);
    
    return grayImage;
}



//改变图片的大小
- (UIImage *)scaleToSize:(UIImage *)img size:(CGSize)size{
    // 创建一个bitmap的context
    // 并把它设置成为当前正在使用的context
    UIGraphicsBeginImageContext(size);
    // 绘制改变大小的图片
    [img drawInRect:CGRectMake(0, 0, size.width, size.height)];
    // 从当前context中创建一个改变大小后的图片
    UIImage* scaledImage = UIGraphicsGetImageFromCurrentImageContext();
    // 使当前的context出堆栈
    UIGraphicsEndImageContext();
    // 返回新的改变大小后的图片
    return scaledImage;
}





- (IBAction)readImageFunc:(id)sender {
    
    
}



@end
