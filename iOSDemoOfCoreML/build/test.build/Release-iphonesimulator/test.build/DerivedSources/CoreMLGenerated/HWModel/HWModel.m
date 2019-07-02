//
// HWModel.m
//
// This file was automatically generated and should not be edited.
//

#import "HWModel.h"

@implementation HWModelInput

- (instancetype)initWithEval_input__0:(MLMultiArray *)eval_input__0 {
    if (self) {
        _eval_input__0 = eval_input__0;
    }
    return self;
}

- (NSSet<NSString *> *)featureNames {
    return [NSSet setWithArray:@[@"eval_input__0"]];
}

- (nullable MLFeatureValue *)featureValueForName:(NSString *)featureName {
    if ([featureName isEqualToString:@"eval_input__0"]) {
        return [MLFeatureValue featureValueWithMultiArray:_eval_input__0];
    }
    return nil;
}

@end

@implementation HWModelOutput

- (instancetype)initWithOp_to_store__0:(MLMultiArray *)op_to_store__0 {
    if (self) {
        _op_to_store__0 = op_to_store__0;
    }
    return self;
}

- (NSSet<NSString *> *)featureNames {
    return [NSSet setWithArray:@[@"op_to_store__0"]];
}

- (nullable MLFeatureValue *)featureValueForName:(NSString *)featureName {
    if ([featureName isEqualToString:@"op_to_store__0"]) {
        return [MLFeatureValue featureValueWithMultiArray:_op_to_store__0];
    }
    return nil;
}

@end

@implementation HWModel

+ (NSURL *)urlOfModelInThisBundle {
    NSString *assetPath = [[NSBundle bundleForClass:[self class]] pathForResource:@"HWModel" ofType:@"mlmodelc"];
    return [NSURL fileURLWithPath:assetPath];
}

- (nullable instancetype)init {
        return [self initWithContentsOfURL:self.class.urlOfModelInThisBundle error:nil];
}

- (nullable instancetype)initWithContentsOfURL:(NSURL *)url error:(NSError * _Nullable * _Nullable)error {
    self = [super init];
    if (!self) { return nil; }
    _model = [MLModel modelWithContentsOfURL:url error:error];
    if (_model == nil) { return nil; }
    return self;
}

- (nullable instancetype)initWithConfiguration:(MLModelConfiguration *)configuration error:(NSError * _Nullable * _Nullable)error {
        return [self initWithContentsOfURL:self.class.urlOfModelInThisBundle configuration:configuration error:error];
}

- (nullable instancetype)initWithContentsOfURL:(NSURL *)url configuration:(MLModelConfiguration *)configuration error:(NSError * _Nullable * _Nullable)error {
    self = [super init];
    if (!self) { return nil; }
    _model = [MLModel modelWithContentsOfURL:url configuration:configuration error:error];
    if (_model == nil) { return nil; }
    return self;
}

- (nullable HWModelOutput *)predictionFromFeatures:(HWModelInput *)input error:(NSError * _Nullable * _Nullable)error {
    return [self predictionFromFeatures:input options:[[MLPredictionOptions alloc] init] error:error];
}

- (nullable HWModelOutput *)predictionFromFeatures:(HWModelInput *)input options:(MLPredictionOptions *)options error:(NSError * _Nullable * _Nullable)error {
    id<MLFeatureProvider> outFeatures = [_model predictionFromFeatures:input options:options error:error];
    return [[HWModelOutput alloc] initWithOp_to_store__0:[outFeatures featureValueForName:@"op_to_store__0"].multiArrayValue];
}

- (nullable HWModelOutput *)predictionFromEval_input__0:(MLMultiArray *)eval_input__0 error:(NSError * _Nullable * _Nullable)error {
    HWModelInput *input_ = [[HWModelInput alloc] initWithEval_input__0:eval_input__0];
    return [self predictionFromFeatures:input_ error:error];
}

- (nullable NSArray<HWModelOutput *> *)predictionsFromInputs:(NSArray<HWModelInput*> *)inputArray options:(MLPredictionOptions *)options error:(NSError * _Nullable * _Nullable)error {
    id<MLBatchProvider> inBatch = [[MLArrayBatchProvider alloc] initWithFeatureProviderArray:inputArray];
    id<MLBatchProvider> outBatch = [_model predictionsFromBatch:inBatch options:options error:error];
    NSMutableArray<HWModelOutput*> *results = [NSMutableArray arrayWithCapacity:(NSUInteger)outBatch.count];
    for (NSInteger i = 0; i < outBatch.count; i++) {
        id<MLFeatureProvider> resultProvider = [outBatch featuresAtIndex:i];
        HWModelOutput * result = [[HWModelOutput alloc] initWithOp_to_store__0:[resultProvider featureValueForName:@"op_to_store__0"].multiArrayValue];
        [results addObject:result];
    }
    return results;
}

@end
