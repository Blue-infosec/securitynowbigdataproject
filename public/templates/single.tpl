<div>
    Episode (format 000, 001, 002, etc...)<input type="text" id="singlesearch" ng-model="singlesearchvalue">
    <div ng-controller="twappController">
        <article data-ng-cloak data-ng-repeat="d in data">
            <securitynow data-twapp="d"></securitynow>
        </article>
    </div>
</div>